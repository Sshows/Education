'use client';

import { Suspense, useCallback, useEffect, useMemo, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  SUBJECT_COMBINATIONS,
  DEMO_PROGRAM_GROUPS,
  type SubjectCombination,
  type SubjectId,
  getRecommendedProgramGroupsForSubjectPair,
  getSubjectCombinationByPair,
  validateProfileSubjectsForProgram,
} from '../../lib/ent-subjects';
import { getTelegramWebApp } from '../../lib/telegram';

type Step = 1 | 2 | 3;

const SCORE_MIN = 50;
const SCORE_MAX = 140;

const comboChips = [
  { short: 'Инфо + Мат', subjects: ['informatics', 'mathematics'] },
  { short: 'Мат + Физ', subjects: ['mathematics', 'physics'] },
  { short: 'Био + Хим', subjects: ['biology', 'chemistry'] },
  { short: 'Физ + Хим', subjects: ['chemistry', 'physics'] },
  { short: 'Ист + Гео', subjects: ['geography', 'world_history'] },
  { short: 'Каз + Лит', subjects: ['kazakh_language', 'kazakh_literature'] },
] as const;

const quotaOptions = [
  { value: 'ordinary', label: 'Общий' },
  { value: 'rural', label: 'Сельская' },
  { value: 'target', label: 'Целевой' },
] as const;

function defaultCombo(): SubjectCombination {
  return (
    getSubjectCombinationByPair('informatics', 'mathematics') ??
    SUBJECT_COMBINATIONS[0]
  );
}

function programsForCombo(combo: SubjectCombination) {
  const codes = getRecommendedProgramGroupsForSubjectPair(combo.subject1, combo.subject2);
  const programs = codes.length > 0
    ? DEMO_PROGRAM_GROUPS.filter((program) => codes.includes(program.code))
    : DEMO_PROGRAM_GROUPS;
  return programs.length ? programs : DEMO_PROGRAM_GROUPS;
}

function firstProgramForCombo(combo: SubjectCombination): string {
  return programsForCombo(combo)[0]?.code ?? 'B057';
}

function CalculatorContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const initialCombo = defaultCombo();
  const [step, setStep] = useState<Step>(1);
  const [score, setScore] = useState(() => Number(searchParams.get('score') ?? 110));
  const [combo, setCombo] = useState<SubjectCombination>(initialCombo);
  const [quota, setQuota] = useState<(typeof quotaOptions)[number]['value']>('ordinary');
  const [program, setProgram] = useState(() => firstProgramForCombo(initialCombo));
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const comboParam = searchParams.get('combo');
    if (!comboParam) return;
    const [a, b] = comboParam.split('+');
    if (!a || !b) return;
    const found = getSubjectCombinationByPair(a as SubjectId, b as SubjectId);
    if (!found) return;
    setCombo(found);
    setProgram(firstProgramForCombo(found));
  }, [searchParams]);

  const availablePrograms = useMemo(() => programsForCombo(combo), [combo]);
  const selectedProgram = availablePrograms.find((item) => item.code === program) ?? availablePrograms[0];
  const subjectMismatch = program ? validateProfileSubjectsForProgram(program, combo.subject1, combo.subject2) : null;
  const scoreValid = Number.isFinite(score) && score >= SCORE_MIN && score <= SCORE_MAX;
  const isValid = scoreValid && Boolean(program) && !subjectMismatch;
  const scorePct = ((score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)) * 100;

  const chooseCombo = (nextCombo: SubjectCombination) => {
    getTelegramWebApp()?.HapticFeedback?.selectionChanged?.();
    setCombo(nextCombo);
    setProgram(firstProgramForCombo(nextCombo));
  };

  const calculate = useCallback(async () => {
    if (!isValid) {
      getTelegramWebApp()?.HapticFeedback?.notificationOccurred?.('warning');
      return;
    }
    const webApp = getTelegramWebApp();
    webApp?.HapticFeedback?.impactOccurred?.('medium');

    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (apiUrl) {
      setSubmitting(true);
      try {
        const response = await fetch(`${apiUrl}/api/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tg_id: webApp?.initDataUnsafe?.user?.id,
            score,
            subject_pair: combo.key,
            quota,
            language: 'ru',
            spec_codes: [program],
          }),
        });
        if (response.ok) {
          const analysis = await response.json();
          sessionStorage.setItem('entGrant:lastAnalysis', JSON.stringify(analysis));
          router.push(
            `/result/${encodeURIComponent(String(analysis.analysis_id ?? 'demo'))}?score=${encodeURIComponent(score)}&program=${encodeURIComponent(program)}&combo=${encodeURIComponent(combo.key)}`,
          );
          return;
        }
      } catch {
        // The Mini App must remain usable even while API is temporarily unavailable.
      } finally {
        setSubmitting(false);
      }
    }

    router.push(
      `/result/demo?score=${encodeURIComponent(score)}&program=${encodeURIComponent(program)}&combo=${encodeURIComponent(combo.key)}`,
    );
  }, [combo.key, isValid, program, quota, router, score]);

  const goNext = () => {
    getTelegramWebApp()?.HapticFeedback?.impactOccurred?.('light');
    if (step === 1) {
      setStep(2);
      return;
    }
    if (step === 2) {
      setStep(3);
      return;
    }
    void calculate();
  };

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const mainButton = webApp?.MainButton;
    if (!mainButton) return;

    const buttonText = step === 3 ? 'Рассчитать' : 'Далее';
    mainButton.setParams?.({
      text: submitting ? 'Считаем...' : buttonText,
      color: '#2878ff',
      text_color: '#ffffff',
      is_active: step !== 2 || Boolean(program),
    });
    if (step !== 2 || Boolean(program)) mainButton.enable?.();
    else mainButton.disable?.();
    mainButton.show();
    webApp?.onEvent?.('mainButtonClicked', goNext);

    return () => {
      webApp?.offEvent?.('mainButtonClicked', goNext);
      mainButton.hide();
    };
  }, [goNext, program, step, submitting]);

  return (
    <main className="grantmeter-screen">
      <header className="gm-header" aria-label="ГрантМетр">
        <div className="gm-logo" aria-hidden="true">G</div>
        <div>
          <strong>ГрантМетр</strong>
          <span>Узнай шансы на грант</span>
        </div>
      </header>

      <nav className="gm-stepper" aria-label="Шаги расчёта">
        {[
          { value: 1, label: 'Балл' },
          { value: 2, label: 'Предметы' },
          { value: 3, label: 'Специальности' },
        ].map((item) => (
          <button
            key={item.value}
            className={step === item.value ? 'gm-step gm-step--active' : step > item.value ? 'gm-step gm-step--done' : 'gm-step'}
            type="button"
            onClick={() => setStep(item.value as Step)}
          >
            <span>{item.value}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {step === 1 && (
        <section className="gm-flow-panel" aria-label="Балл и профиль">
          <p className="gm-label">Балл ЕНТ</p>
          <div className="gm-score-card" style={{ '--score-pct': `${scorePct}%` } as React.CSSProperties}>
            <strong>{score}</strong>
            <div className="gm-score-range">
              <span className="gm-score-bubble">{score}</span>
              <input
                aria-label="Балл ЕНТ"
                max={SCORE_MAX}
                min={SCORE_MIN}
                type="range"
                value={score}
                onChange={(event) => setScore(Number(event.target.value))}
              />
              <div className="gm-range-labels">
                <span>{SCORE_MIN}</span>
                <span>{SCORE_MAX}</span>
              </div>
            </div>
          </div>

          <p className="gm-label">Проф. предметы</p>
          <div className="gm-chip-grid" aria-label="Профильные предметы">
            {comboChips.map((chip) => {
              const chipCombo = getSubjectCombinationByPair(chip.subjects[0], chip.subjects[1]);
              if (!chipCombo) return null;
              const selected = chipCombo.key === combo.key;
              return (
                <button
                  className={selected ? 'gm-chip gm-chip--active' : 'gm-chip'}
                  key={chip.short}
                  type="button"
                  onClick={() => chooseCombo(chipCombo)}
                >
                  {chip.short}
                </button>
              );
            })}
          </div>

          <p className="gm-label">Квота</p>
          <div className="gm-segmented" role="tablist" aria-label="Квота">
            {quotaOptions.map((item) => (
              <button
                className={quota === item.value ? 'gm-segment gm-segment--active' : 'gm-segment'}
                key={item.value}
                type="button"
                onClick={() => setQuota(item.value)}
              >
                {item.label}
              </button>
            ))}
          </div>
        </section>
      )}

      {step === 2 && (
        <section className="gm-flow-panel" aria-label="Выбор специальности">
          <p className="gm-label">Специальность</p>
          <h1 className="gm-panel-title">{combo.label.ru}</h1>
          <div className="gm-program-list">
            {availablePrograms.slice(0, 7).map((item) => (
              <button
                className={program === item.code ? 'gm-program gm-program--active' : 'gm-program'}
                key={item.code}
                type="button"
                onClick={() => setProgram(item.code)}
              >
                <span>{item.code}</span>
                <strong>{item.name.ru}</strong>
                <small>{item.category}</small>
              </button>
            ))}
          </div>
          {subjectMismatch && <p className="gm-warning">{subjectMismatch}</p>}
        </section>
      )}

      {step === 3 && (
        <section className="gm-flow-panel" aria-label="Проверка перед расчётом">
          <p className="gm-label">Проверка</p>
          <div className="gm-summary">
            <div>
              <span>Балл</span>
              <strong>{score}</strong>
            </div>
            <div>
              <span>Предметы</span>
              <strong>{combo.label.ru}</strong>
            </div>
            <div>
              <span>Программа</span>
              <strong>{selectedProgram?.code} · {selectedProgram?.name.ru}</strong>
            </div>
            <div>
              <span>Квота</span>
              <strong>{quotaOptions.find((item) => item.value === quota)?.label}</strong>
            </div>
          </div>
          <p className="gm-note">
            Первый расчёт бесплатный. Полный разбор, источники и рекомендации откроются в Premium.
          </p>
        </section>
      )}

      <button
        className="gm-primary-cta"
        disabled={submitting || (step === 2 && !program)}
        type="button"
        onClick={goNext}
      >
        {submitting ? 'Считаем...' : step === 3 ? 'Рассчитать' : 'Далее'}
        <span aria-hidden="true">→</span>
      </button>

      <p className="gm-footer-note">Шаг {step} из 3 · бесплатно</p>
    </main>
  );
}

export default function CalculatorPage() {
  return (
    <Suspense fallback={
      <main className="grantmeter-screen">
        <div className="gm-skeleton gm-skeleton-title" />
        <div className="gm-skeleton gm-skeleton-card" />
      </main>
    }>
      <CalculatorContent />
    </Suspense>
  );
}
