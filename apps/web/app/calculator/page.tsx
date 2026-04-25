'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { postForecast } from '../../lib/api';
import { initTelegramWebApp } from '../../lib/telegram';

export default function CalculatorPage() {
  const router = useRouter();
  const [total, setTotal] = useState(82);

  useEffect(() => {
    const app = initTelegramWebApp();
    if (app?.MainButton) {
      app.MainButton.setText('Рассчитать шанс');
      app.MainButton.show();
      app.MainButton.onClick(() => void onSubmit());
    }
  }, []);

  async function onSubmit() {
    const result = await postForecast({
      profile: {
        total_score: total,
        kazakhstan_history_score: 10,
        math_literacy_score: 10,
        reading_literacy_score: 10,
        profile_subject_1: 'Mathematics',
        profile_subject_1_score: 30,
        profile_subject_2: 'Informatics',
        profile_subject_2_score: 30,
        subject_combo: 'Math+Informatics',
        region: 'Алматы',
        locality_type: 'city',
        quota_category: 'ordinary',
        language: 'ru',
        target: 'both',
      },
      university_id: 1,
      program_group_id: 1,
    });
    sessionStorage.setItem('latest_forecast', JSON.stringify(result));
    router.push('/result/latest');
  }

  return (
    <main>
      <h2>Калькулятор ЕНТ</h2>
      <div className="card">
        <label>Общий балл ЕНТ (0-140)</label>
        <input value={total} min={0} max={140} onChange={(e) => setTotal(Number(e.target.value))} type="number" />
      </div>
      <div className="card">Профильные предметы: Mathematics + Informatics (MVP demo)</div>
      <div className="card">Квота: ordinary (MVP demo)</div>
      <div className="card">Вуз: IITU, программа: B057 (MVP demo)</div>
      <button className="button" onClick={() => void onSubmit()}>Рассчитать шанс</button>
    </main>
  );
}
