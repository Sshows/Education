import { ConflictWarning } from '../../../components/ConflictWarning';
import { ErrorMarginWarning } from '../../../components/ErrorMarginWarning';
import { ProbabilityGauge } from '../../../components/ProbabilityGauge';
import { SourceBadge } from '../../../components/SourceBadge';

const probability = 64;
const score = 82;
const cutoff = 78;
const errorMargin = 9;

export default function ResultPage() {
  const scoreWidth = Math.min(100, Math.round((score / 140) * 100));
  const cutoffWidth = Math.min(100, Math.round((cutoff / 140) * 100));

  return (
    <main>
      <p className="eyebrow">Результат</p>
      <h1 className="page-title">Шанс выше среднего</h1>
      <p className="page-subtitle">Демо-прогноз для B057 и МУИТ: используйте его как ориентир перед официальным конкурсом.</p>

      <section className="result-hero">
        <ProbabilityGauge value={probability} />
        <div className="grid">
          <div className="metric">
            <span className="small">Ваш балл</span>
            <strong>{score}</strong>
          </div>
          <div className="metric">
            <span className="small">Ориентир прошлого конкурса</span>
            <strong>{cutoff}</strong>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Score vs cutoff</h2>
        <p>Балл выше демо-ориентира на {score - cutoff} пункта, но итог зависит от заявлений и квот.</p>
        <div className="score-bar" aria-label="Ваш балл">
          <span style={{ width: `${scoreWidth}%` }} />
        </div>
        <p className="small">Ориентир cutoff: {cutoffWidth}% шкалы ЕНТ</p>
      </section>

      <section className="card">
        <h2>Confidence</h2>
        <p><span className="confidence-badge">medium</span></p>
        <p>Погрешность выше обычной, если по программе мало свежих официальных данных.</p>
      </section>

      <ConflictWarning />

      <section className="card">
        <h2>Sources</h2>
        <div className="program-card__meta">
          <SourceBadge label="НЦТ" />
          <SourceBadge label="МНВО" />
          <SourceBadge label="приёмная комиссия" />
        </div>
      </section>

      <ErrorMarginWarning errorMargin={errorMargin} />
    </main>
  );
}
