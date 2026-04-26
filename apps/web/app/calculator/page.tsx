'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';

import { getTelegramWebApp } from '../../lib/telegram';

export default function CalculatorPage() {
  const router = useRouter();
  const [score, setScore] = useState('82');
  const [subjectOne, setSubjectOne] = useState('Математика');
  const [subjectTwo, setSubjectTwo] = useState('Информатика');
  const [quota, setQuota] = useState('ordinary');
  const [language, setLanguage] = useState('ru');
  const [university, setUniversity] = useState('МУИТ / IITU');
  const [program, setProgram] = useState('B057');

  const totalScore = Number(score);
  const isValid = Boolean(score.trim() !== '' && Number.isFinite(totalScore) && totalScore >= 0 && totalScore <= 140 && subjectOne && subjectTwo && university && program);
  const progress = useMemo(() => {
    const checks = [score, subjectOne, subjectTwo, quota, language, university, program].filter(Boolean).length;
    return Math.round((checks / 7) * 100);
  }, [language, program, quota, score, subjectOne, subjectTwo, university]);

  const calculate = useCallback(() => {
    if (!isValid) {
      getTelegramWebApp()?.HapticFeedback?.notificationOccurred?.('warning');
      return;
    }
    getTelegramWebApp()?.HapticFeedback?.impactOccurred?.('medium');
    router.push(`/result/demo?score=${encodeURIComponent(score)}&program=${encodeURIComponent(program)}`);
  }, [isValid, program, router, score]);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const mainButton = webApp?.MainButton;
    if (!mainButton) {
      return;
    }

    mainButton.setParams?.({
      text: isValid ? 'Рассчитать' : 'Заполните поля',
      color: '#0f766e',
      text_color: '#ffffff',
      is_active: isValid,
    });
    if (isValid) {
      mainButton.enable?.();
    } else {
      mainButton.disable?.();
    }
    mainButton.show();
    webApp?.onEvent?.('mainButtonClicked', calculate);

    return () => {
      webApp?.offEvent?.('mainButtonClicked', calculate);
      mainButton.hide();
    };
  }, [calculate, isValid]);

  return (
    <main>
      <p className="eyebrow">Калькулятор</p>
      <h1 className="page-title">Расчёт шанса</h1>
      <p className="page-subtitle">Заполните профиль ЕНТ, чтобы получить демо-прогноз с источниками и погрешностью.</p>

      <div className="wizard">
        <div className="progress" aria-label="Прогресс заполнения">
          <span style={{ width: `${progress}%` }} />
        </div>

        <section className="wizard-step">
          <p className="eyebrow">Step 1: Баллы</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="score">Общий балл ЕНТ</label>
              <input id="score" inputMode="numeric" max="140" min="0" type="number" value={score} onChange={(event) => setScore(event.target.value)} />
            </div>
            <div className="metric">
              <span className="small">Ориентир конкурса</span>
              <strong>{Number.isFinite(totalScore) ? `${totalScore}/140` : '0/140'}</strong>
            </div>
          </div>
        </section>

        <section className="wizard-step">
          <p className="eyebrow">Step 2: Профильные предметы</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="subjectOne">Первый предмет</label>
              <select id="subjectOne" value={subjectOne} onChange={(event) => setSubjectOne(event.target.value)}>
                <option>Математика</option>
                <option>Физика</option>
                <option>География</option>
                <option>Биология</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="subjectTwo">Второй предмет</label>
              <select id="subjectTwo" value={subjectTwo} onChange={(event) => setSubjectTwo(event.target.value)}>
                <option>Информатика</option>
                <option>Физика</option>
                <option>Химия</option>
                <option>Английский язык</option>
              </select>
            </div>
          </div>
        </section>

        <section className="wizard-step">
          <p className="eyebrow">Step 3: Квота, регион, язык</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="quota">Категория</label>
              <select id="quota" value={quota} onChange={(event) => setQuota(event.target.value)}>
                <option value="ordinary">Общий конкурс</option>
                <option value="rural">Сельская квота</option>
                <option value="social">Социальная квота</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="language">Язык обучения</label>
              <select id="language" value={language} onChange={(event) => setLanguage(event.target.value)}>
                <option value="ru">Русский</option>
                <option value="kk">Казахский</option>
                <option value="en">Английский</option>
              </select>
            </div>
          </div>
        </section>

        <section className="wizard-step">
          <p className="eyebrow">Step 4: Вуз и программа</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="university">Вуз</label>
              <select id="university" value={university} onChange={(event) => setUniversity(event.target.value)}>
                <option>МУИТ / IITU</option>
                <option>Astana IT University</option>
                <option>SDU University</option>
                <option>KBTU</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="program">Программа</label>
              <select id="program" value={program} onChange={(event) => setProgram(event.target.value)}>
                <option>B057</option>
                <option>B058</option>
                <option>B059</option>
                <option>B157</option>
              </select>
            </div>
          </div>
        </section>

        <section className="wizard-step">
          <p className="eyebrow">Step 5: Результат</p>
          <p className="hint">Telegram MainButton и нижняя кнопка ведут на страницу результата. API можно подключить позже без смены сценария.</p>
        </section>
      </div>

      <div className="sticky-action">
        <button className="button" disabled={!isValid} onClick={calculate}>Рассчитать</button>
        {!isValid ? <span className="small">Проверьте балл и обязательные поля.</span> : null}
      </div>
    </main>
  );
}
