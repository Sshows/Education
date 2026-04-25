import Link from 'next/link';

export default function HomePage() {
  return (
    <main>
      <h1>ent-grant-telegram</h1>
      <Link className="button" href="/calculator">Рассчитать шанс</Link>
      <Link className="button" href="/universities">Найти университет</Link>
      <Link className="button" href="/programs">Подобрать программу</Link>
      <Link className="button" href="/ai">Спросить AI-консультанта</Link>
      <Link className="button" href="/deadlines">Дедлайны и правила</Link>
    </main>
  );
}
