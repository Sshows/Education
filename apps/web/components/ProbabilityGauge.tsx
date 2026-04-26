import type { CSSProperties } from 'react';

export function ProbabilityGauge({ value }: { value: number }) {
  const label = value <= 20 ? 'очень низкий' : value <= 40 ? 'низкий' : value <= 60 ? 'средний' : value <= 80 ? 'высокий' : 'очень высокий';

  return (
    <div className="probability-ring" style={{ '--value': `${value}%` } as CSSProperties}>
      <div className="probability-ring__inner">
        <div>
          <strong>{value}%</strong>
          <span className="small">{label}</span>
        </div>
      </div>
    </div>
  );
}
