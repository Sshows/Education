import Link from 'next/link';

type Program = {
  code: string;
  name: string;
  subjects: string;
  cutoff: number;
  demand: string;
};

export function ProgramCard({ program }: { program: Program }) {
  return (
    <Link className="program-card" href={`/programs/${program.code.toLowerCase()}`}>
      <span className="tag">{program.code}</span>
      <h2>{program.name}</h2>
      <p>{program.subjects}</p>
      <div className="program-card__meta">
        <span className="tag">ориентир {program.cutoff}+</span>
        <span className="tag">{program.demand}</span>
      </div>
    </Link>
  );
}
