import { ErrorMarginWarning } from '../../../components/ErrorMarginWarning';
import { ProbabilityGauge } from '../../../components/ProbabilityGauge';

export default function ResultPage() {
  return (
    <main>
      <h2>Результат расчёта</h2>
      <div className="card">Статус: eligible_for_competition</div>
      <ProbabilityGauge value={34} />
      <div className="card">Платное обучение: eligible</div>
      <div className="card">Confidence: medium</div>
      <div className="card">Есть расхождение в источниках</div>
      <ErrorMarginWarning errorMargin={12} />
    </main>
  );
}
