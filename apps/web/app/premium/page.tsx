import Link from 'next/link';

export default function PremiumPage() {
  return (
    <main>
      <p className="eyebrow">Premium</p>
      <h1 className="page-title">Полный доступ к прогнозам</h1>
      <p className="page-subtitle">Premium открывает сравнения вузов, расширенные рекомендации, AI-лимиты и сохранённый профиль.</p>
      <section className="card">
        <h2>Что входит</h2>
        <ul className="feature-list">
          <li>Полный forecast с confidence explanation</li>
          <li>Score vs cutoff и source breakdown</li>
          <li>100 AI-вопросов на месяц</li>
          <li>Алерты по дедлайнам</li>
        </ul>
      </section>
      <Link className="button" href="/pricing">Выбрать тариф</Link>
    </main>
  );
}
