import { sources } from '../../lib/demo-data';

export default function SourcesPage() {
  return (
    <main>
      <p className="eyebrow">Данные</p>
      <h1 className="page-title">Источники</h1>
      <p className="page-subtitle">Каждый прогноз должен ссылаться на открытый источник и дату обновления.</p>

      <section className="catalog-grid">
        {sources.map((source) => (
          <a className="source-row" href={source.url} key={source.title}>
            <h2>{source.title}</h2>
            <p>{source.status}</p>
          </a>
        ))}
      </section>
    </main>
  );
}
