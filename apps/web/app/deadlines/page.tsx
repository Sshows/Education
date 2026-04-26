import { deadlines } from '../../lib/demo-data';

export default function DeadlinesPage() {
  return (
    <main>
      <p className="eyebrow">Поступление</p>
      <h1 className="page-title">Дедлайны</h1>
      <p className="page-subtitle">Перед финальной подачей сверяйте даты с официальными публикациями НЦТ, МНВО и вузов.</p>

      <section className="catalog-grid">
        {deadlines.map((item) => (
          <article className="deadline-row" key={item.title}>
            <h2>{item.title}</h2>
            <p>{item.period}</p>
            <span className="tag">{item.source}</span>
          </article>
        ))}
      </section>
    </main>
  );
}
