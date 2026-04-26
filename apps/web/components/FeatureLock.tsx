import Link from 'next/link';

export function FeatureLock({ title, text }: { title: string; text: string }) {
  return (
    <section className="card premium-lock">
      <span className="premium-lock__label">Premium</span>
      <h2>{title}</h2>
      <p>{text}</p>
      <Link className="button" href="/pricing">Разблокировать полный прогноз</Link>
    </section>
  );
}
