import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'ENT Grant — Шанс поступления по ЕНТ',
  description:
    'Рассчитай шанс поступления на грант или платное по ЕНТ. Калькулятор с историческими данными, вузами Казахстана и программами.',
};

const featureCards = [
  {
    href: '/calculator',
    emoji: '🎯',
    title: 'Калькулятор ЕНТ',
    text: 'Балл, предметы, квота, вуз и программа — всё в одном расчёте с погрешностью.',
  },
  {
    href: '/universities',
    emoji: '🏛',
    title: 'Вузы',
    text: 'Вузы Казахстана с проходными баллами и специализацией.',
  },
  {
    href: '/programs',
    emoji: '📋',
    title: 'Программы',
    text: 'B057, B058, B059, B074, B086 и другие — с предметными парами.',
  },
  {
    href: '/ai',
    emoji: '🤖',
    title: 'AI-консультант',
    text: 'Ответы только с источниками и честной формулировкой.',
  },
  {
    href: '/deadlines',
    emoji: '📅',
    title: 'Дедлайны',
    text: 'Что проверить перед подачей заявления.',
  },
];

const combos = [
  { alias: 'физмат', label: 'Матем + Физика', href: '/programs?combo=mathematics%2Bphysics' },
  { alias: 'инфомат', label: 'Матем + Информатика', href: '/programs?combo=informatics%2Bmathematics' },
  { alias: 'химбио', label: 'Биология + Химия', href: '/programs?combo=biology%2Bchemistry' },
  { alias: 'истправо', label: 'История + Право', href: '/programs?combo=fundamentals_of_law%2Bworld_history' },
  { alias: 'матгео', label: 'Матем + География', href: '/programs?combo=geography%2Bmathematics' },
];

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <p className="eyebrow">ENT Grant KZ</p>
        <h1>Узнай шанс на грант по ЕНТ</h1>
        <p>
          Ориентировочный прогноз поступления по открытым данным НЦТ и МНВО.
          Не гарантия — отправная точка для правильного выбора.
        </p>
        <div className="actions">
          <Link className="button" href="/calculator">
            🎯 Рассчитать шанс
          </Link>
          <Link className="secondary-button" href="/universities">
            🏛 Вузы
          </Link>
        </div>
      </section>

      {/* Quick combo shortcuts */}
      <div className="chips" aria-label="Комбинации предметов">
        {combos.map((c) => (
          <Link className="chip" href={c.href} key={c.alias}>
            {c.label}
          </Link>
        ))}
      </div>

      {/* Feature cards */}
      <section className="grid grid--two" aria-label="Ключевые разделы">
        {featureCards.map((card) => (
          <Link className="card" href={card.href} key={card.href}>
            <div style={{ fontSize: 28, marginBottom: 6 }}>{card.emoji}</div>
            <h2>{card.title}</h2>
            <p>{card.text}</p>
          </Link>
        ))}
      </section>

      {/* Demo example */}
      <section className="card example-card" aria-label="Пример прогноза" style={{ marginTop: 12 }}>
        <p className="eyebrow" style={{ color: 'rgba(255,255,255,0.5)' }}>Пример</p>
        <h2>82 балла, B057, МУИТ</h2>
        <p>
          Прогноз с погрешностью ±9 п.п. и источниками показывает,
          где шанс сильнее и что стоит уточнить перед заявкой.
        </p>
        <Link
          className="button"
          href="/result/demo?score=82&program=B057"
          style={{ marginTop: 14, display: 'inline-flex', fontSize: 13 }}
        >
          Посмотреть пример ›
        </Link>
      </section>

      {/* Disclaimer snippet */}
      <section className="disclaimer" style={{ marginTop: 12 }} aria-label="Дисклеймер">
        <p>
          ⚠️ Данные — демонстрационные. Реальный результат конкурса зависит
          от официальных решений НЦТ, МНВО, квот и заявлений других абитуриентов.
        </p>
      </section>
    </main>
  );
}
