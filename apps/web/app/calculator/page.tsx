'use client';

import { Suspense, useCallback, useEffect, useMemo, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  SUBJECT_COMBINATIONS,
  DEMO_PROGRAM_GROUPS,
  type SubjectId,
  type SubjectCombination,
  getSubjectCombinationByPair,
  getRecommendedProgramGroupsForSubjectPair,
  validateProfileSubjectsForProgram,
  getSubjectCombinationByAlias,
} from '../../lib/ent-subjects';
import { getTelegramWebApp } from '../../lib/telegram';

type Step = 1 | 2 | 3 | 4;

function CalculatorContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [step, setStep] = useState<Step>(1);
  const [score, setScore] = useState(searchParams.get('score') ?? '');
  const [aliasInput, setAliasInput] = useState('');
  const [combo, setCombo] = useState<SubjectCombination | null>(null);
  const [quota, setQuota] = useState('ordinary');
  const [language, setLanguage] = useState('ru');
  const [program, setProgram] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // If URL has a combo param, auto-select it
  useEffect(() => {
    const comboParam = searchParams.get('combo');
    if (comboParam) {
      const [a, b] = comboParam.split('+');
      if (a && b) {
        const found = getSubjectCombinationByPair(a as SubjectId, b as SubjectId);
        if (found) setCombo(found);
      }
    }
  }, [searchParams]);

  const totalScore = parseInt(score, 10);
  const scoreValid = score !== '' && Number.isFinite(totalScore) && totalScore >= 0 && totalScore <= 140;

  // Programs available for the selected combo
  const availablePrograms = useMemo(() => {
    if (!combo) return DEMO_PROGRAM_GROUPS;
    const codes = getRecommendedProgramGroupsForSubjectPair(combo.subject1, combo.subject2);
    if (codes.length === 0) return DEMO_PROGRAM_GROUPS;
    return DEMO_PROGRAM_GROUPS.filter((p) => codes.includes(p.code));
  }, [combo]);

  // Subject mismatch validation
  const subjectMismatch = useMemo(() => {
    if (!program || !combo) return null;
    return validateProfileSubjectsForProgram(program, combo.subject1, combo.subject2);
  }, [program, combo]);

  const isValid = scoreValid && combo !== null && program !== '' && subjectMismatch === null;

  // progress: 4 steps
  const stepsDone = useMemo(() => {
    let done = 0;
    if (scoreValid) done++;
    if (combo) done++;
    if (quota && language) done++;
    if (program && !subjectMismatch) done++;
    return done;
  }, [scoreValid, combo, quota, language, program, subjectMismatch]);

  // Alias search
  const handleAliasSearch = useCallback((value: string) => {
    setAliasInput(value);
    const found = getSubjectCombinationByAlias(value.trim());
    if (found) setCombo(found);
  }, []);

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
            score: totalScore,
            subject_pair: combo!.key,
            quota,
            language,
            spec_codes: [program],
          }),
        });
        if (response.ok) {
          const analysis = await response.json();
          sessionStorage.setItem('entGrant:lastAnalysis', JSON.stringify(analysis));
          router.push(
            `/result/${encodeURIComponent(String(analysis.analysis_id ?? 'demo'))}?score=${encodeURIComponent(score)}&program=${encodeURIComponent(program)}&combo=${encodeURIComponent(combo!.key)}`,
          );
          return;
        }
      } catch {
        // Keep the local demo result available if API is temporarily unreachable.
      } finally {
        setSubmitting(false);
      }
    }
    router.push(
      `/result/demo?score=${encodeURIComponent(score)}&program=${encodeURIComponent(program)}&combo=${encodeURIComponent(combo!.key)}`,
    );
  }, [combo, isValid, language, program, quota, router, score, totalScore]);

  // Telegram MainButton
  useEffect(() => {
    const webApp = getTelegramWebApp();
    const mainButton = webApp?.MainButton;
    if (!mainButton) return;

    mainButton.setParams?.({
      text: isValid ? 'Рассчитать шанс' : 'Заполните все поля',
      color: isValid ? '#4f7cff' : '#374151',
      text_color: '#ffffff',
      is_active: isValid,
    });
    if (isValid) mainButton.enable?.();
    else mainButton.disable?.();
    mainButton.show();
    webApp?.onEvent?.('mainButtonClicked', calculate);

    return () => {
      webApp?.offEvent?.('mainButtonClicked', calculate);
      mainButton.hide();
    };
  }, [calculate, isValid]);

  return (
    <main>
      <p className="eyebrow">Калькулятор ЕНТ</p>
      <h1 className="page-title">Расчёт шанса</h1>
      <p className="page-subtitle">
        Заполните профиль ЕНТ — получите демо-прогноз с источниками и погрешностью.
      </p>

      {/* Step progress dots */}
      <div className="step-progress" role="progressbar" aria-valuenow={stepsDone} aria-valuemax={4}>
        {[1, 2, 3, 4].map((s) => (
          <div
            key={s}
            className={`step-dot ${s < stepsDone + 1 ? 'step-dot--done' : ''} ${s === step ? 'step-dot--active' : ''}`}
          />
        ))}
        <span className="small" style={{ marginLeft: 8 }}>
          Шаг {Math.min(stepsDone + 1, 4)} из 4
        </span>
      </div>

      {/* Linear progress bar */}
      <div className="progress" aria-hidden="true">
        <span style={{ width: `${(stepsDone / 4) * 100}%` }} />
      </div>

      <div className="wizard">
        {/* ---- STEP 1: Score ---- */}
        <section className="wizard-step" id="step-score">
          <p className="eyebrow">Шаг 1 — Баллы</p>
          <p className="small" style={{ marginTop: 4 }}>
            Введите общий балл ЕНТ (0–140).
          </p>
          <div className="field-grid" style={{ gridTemplateColumns: '1fr 1fr', marginTop: 12 }}>
            <div className="field">
              <label htmlFor="score">Балл ЕНТ</label>
              <input
                id="score"
                inputMode="numeric"
                max="140"
                min="0"
                type="number"
                value={score}
                placeholder="82"
                onChange={(e) => { setScore(e.target.value); setStep(1); }}
              />
            </div>
            <div className="metric" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <span className="small">Прогресс</span>
              <strong style={{ fontSize: 20 }}>
                {scoreValid ? `${totalScore}/140` : '—/140'}
              </strong>
              {scoreValid && totalScore >= 50 && (
                <span className="small" style={{ color: 'var(--success)' }}>✓ Принято</span>
              )}
            </div>
          </div>
        </section>

        {/* ---- STEP 2: Subject combo ---- */}
        <section className="wizard-step" id="step-subjects">
          <p className="eyebrow">Шаг 2 — Профильные предметы</p>
          <p className="small" style={{ marginTop: 4 }}>
            Выберите комбинацию из двух профильных предметов ЕНТ.
          </p>

          {/* Alias quick-search */}
          <div className="field" style={{ marginTop: 12 }}>
            <label htmlFor="alias-search">Быстрый поиск (физмат, инфомат, химбио…)</label>
            <input
              id="alias-search"
              className="search-input"
              type="text"
              placeholder="Например: инфомат"
              value={aliasInput}
              onChange={(e) => handleAliasSearch(e.target.value)}
              style={{ width: '100%', minHeight: 48 }}
            />
          </div>

          {/* Combination picker */}
          <div className="combo-picker" style={{ marginTop: 12 }}>
            {SUBJECT_COMBINATIONS.map((c) => {
              const isSelected = combo?.key === c.key;
              return (
                <button
                  key={c.key}
                  className={`combo-option ${isSelected ? 'combo-option--selected' : ''}`}
                  onClick={() => { setCombo(c); setProgram(''); setStep(2); }}
                  type="button"
                >
                  <div>
                    <div className="combo-option__label">{c.label.ru}</div>
                    <div className="combo-option__cat">{c.category.ru}</div>
                  </div>
                  {isSelected && <span className="combo-option__check">✓</span>}
                </button>
              );
            })}
          </div>
        </section>

        {/* ---- STEP 3: Quota & language ---- */}
        <section className="wizard-step" id="step-quota">
          <p className="eyebrow">Шаг 3 — Квота и язык</p>
          <div className="field-grid" style={{ marginTop: 12 }}>
            <div className="field">
              <label htmlFor="quota">Категория</label>
              <select id="quota" value={quota} onChange={(e) => setQuota(e.target.value)}>
                <option value="ordinary">Общий конкурс</option>
                <option value="rural">Сельская квота</option>
                <option value="social">Социальная квота</option>
                <option value="orphan">Дети-сироты</option>
                <option value="disability">Лица с инвалидностью</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="language">Язык обучения</label>
              <select id="language" value={language} onChange={(e) => setLanguage(e.target.value)}>
                <option value="ru">Русский</option>
                <option value="kk">Казахский</option>
                <option value="en">Английский</option>
              </select>
            </div>
          </div>
        </section>

        {/* ---- STEP 4: University & Program ---- */}
        <section className="wizard-step" id="step-program">
          <p className="eyebrow">Шаг 4 — Программа</p>
          {combo ? (
            <>
              <p className="small" style={{ marginTop: 4 }}>
                Программы для <strong>{combo.label.ru}</strong>:
              </p>
              <div className="field" style={{ marginTop: 10 }}>
                <label htmlFor="program">Группа ОП (код)</label>
                <select
                  id="program"
                  value={program}
                  onChange={(e) => { setProgram(e.target.value); setStep(4); }}
                >
                  <option value="">— Выберите программу —</option>
                  {availablePrograms.map((p) => (
                    <option key={p.code} value={p.code}>
                      {p.code} — {p.name.ru}
                    </option>
                  ))}
                </select>
              </div>
              {/* Subject mismatch warning */}
              {subjectMismatch && (
                <div className="mismatch-warning" style={{ marginTop: 10 }}>
                  <strong>⚠ Несовместимость:</strong> {subjectMismatch}
                </div>
              )}
              {/* Demo data badge */}
              <div style={{ marginTop: 10 }}>
                <span className="demo-badge">⚠ Демо-данные</span>
                <span className="small" style={{ marginLeft: 8 }}>
                  Подключите API для официальных данных
                </span>
              </div>
            </>
          ) : (
            <p className="small" style={{ marginTop: 8, color: 'var(--warning)' }}>
              Сначала выберите комбинацию предметов в шаге 2.
            </p>
          )}
        </section>
      </div>

      {/* Sticky CTA */}
      <div className="sticky-action">
        <button
          className="button"
          disabled={!isValid || submitting}
          onClick={calculate}
          style={{ width: '100%' }}
          type="button"
        >
          {submitting ? 'Считаем...' : isValid ? '🎯 Рассчитать шанс' : 'Заполните все поля'}
        </button>
        {!isValid && (
          <p className="small" style={{ textAlign: 'center', marginTop: 4 }}>
            {!scoreValid && '• Введите балл ЕНТ (0–140). '}
            {!combo && '• Выберите комбинацию предметов. '}
            {combo && !program && '• Выберите программу. '}
            {subjectMismatch && '• Предметы не совпадают с программой. '}
          </p>
        )}
      </div>
    </main>
  );
}

export default function CalculatorPage() {
  return (
    <Suspense fallback={
      <main>
        <div className="skeleton skeleton-title" style={{ marginTop: 20 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 12 }} />
      </main>
    }>
      <CalculatorContent />
    </Suspense>
  );
}
