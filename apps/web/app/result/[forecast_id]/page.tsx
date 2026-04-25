'use client';

import { useEffect, useState } from 'react';

import { ErrorMarginWarning } from '../../../components/ErrorMarginWarning';
import { ProbabilityGauge } from '../../../components/ProbabilityGauge';

export default function ResultPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const raw = sessionStorage.getItem('latest_forecast');
    if (raw) setData(JSON.parse(raw));
  }, []);

  if (!data) return <main><h2>Результат</h2><div className="card">нет подтверждённых данных</div></main>;

  return (
    <main>
      <h2>Результат расчёта</h2>
      <ProbabilityGauge value={data.grant_probability} />
      <div className="card">Статус гранта: {data.grant_status}</div>
      <div className="card">Статус платного: {data.paid_status}</div>
      <div className="card">Confidence: {data.confidence}</div>
      <div className="card">Погрешность: ±{data.error_margin_pp} п.п.</div>
      <div className="card">Причины: {(data.explanation?.confidence_reasons || []).join(', ') || 'нет подтверждённых данных'}</div>
      {(data.explanation?.conflicts || []).length > 0 && <div className="card">Есть расхождение в источниках</div>}
      <div className="card">
        Источники:
        <ul>
          {(data.sources || []).map((s: any) => (
            <li key={s.id || s.url}>{s.url} — {s.publisher || 'нет подтверждённых данных'} — confidence: {s.confidence || 'unknown'}</li>
          ))}
          {(data.sources || []).length === 0 && <li>нет подтверждённых данных</li>}
        </ul>
      </div>
      <ErrorMarginWarning errorMargin={data.error_margin_pp} />
    </main>
  );
}
