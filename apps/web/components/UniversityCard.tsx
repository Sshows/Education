import Link from 'next/link';

type University = {
  id: string;
  name: string;
  city: string;
  focus: string;
  cutoff: number;
};

export function UniversityCard({ university }: { university: University }) {
  return (
    <Link className="university-card" href={`/universities/${university.id}`}>
      <span className="tag">{university.city}</span>
      <h2>{university.name}</h2>
      <p>{university.focus}</p>
      <div className="university-card__meta">
        <span className="tag">прошлый ориентир {university.cutoff}+</span>
        <span className="tag">доступен в расчёте</span>
      </div>
    </Link>
  );
}
