import Link from 'next/link';

export default function UniversityCardPage() {
  return (
    <main>
      <p className="eyebrow">Вуз</p>
      <h1 className="page-title">МУИТ / IITU</h1>
      <section className="card">
        <h2>Что проверить</h2>
        <p>Порог, язык обучения, стоимость, гранты, творческие требования и дату обновления источника.</p>
      </section>
      <Link className="button" href="/calculator">Проверить с моим баллом</Link>
    </main>
  );
}
