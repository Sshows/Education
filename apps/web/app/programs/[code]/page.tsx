import Link from 'next/link';

export default function ProgramPage() {
  return (
    <main>
      <p className="eyebrow">Программа</p>
      <h1 className="page-title">B057 Информационные технологии</h1>
      <section className="card">
        <h2>Профиль</h2>
        <p>Математика + информатика. Подходит для software, data, product и инженерных IT-треков.</p>
      </section>
      <Link className="button" href="/calculator">Рассчитать шанс</Link>
    </main>
  );
}
