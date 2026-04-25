export function ProbabilityGauge({ value }: { value: number }) {
  const text = value <= 20 ? 'очень низкий' : value <= 40 ? 'низкий' : value <= 60 ? 'средний' : value <= 80 ? 'высокий' : 'очень высокий';
  return <div className="card"><strong>{value}%</strong> — {text}</div>;
}
