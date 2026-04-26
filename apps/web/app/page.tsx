import Link from 'next/link';

const featureCards = [
  { href: '/calculator', title: 'Калькулятор ЕНТ', text: 'Балл, предметы, квота, язык и выбранная программа в одном расчёте.' },
  { href: '/universities', title: 'Вузы', text: 'Быстрый список сильных вариантов по городу и профилю.' },
  { href: '/programs', title: 'Программы', text: 'Группы B057, B058, B059, B157 с предметами и ориентирами.' },
  { href: '/ai', title: 'AI-консультант', text: 'Ответы только с пометкой источников и осторожной формулировкой.' },
  { href: '/deadlines', title: 'Дедлайны', text: 'Что проверить перед подачей заявления и творческими экзаменами.' },
];

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <p className="eyebrow">ENT Grant</p>
        <h1>Узнай шанс на грант по ЕНТ</h1>
        <p>Мини-прогноз для выбора вуза, программы и следующего шага без лишней суеты.</p>
        <div className="actions">
          <Link className="button" href="/calculator">Рассчитать шанс</Link>
          <Link className="secondary-button" href="/universities">Подобрать вуз</Link>
        </div>
      </section>

      <section className="grid grid--two" aria-label="Ключевые действия">
        {featureCards.map((card) => (
          <Link className="card" href={card.href} key={card.href}>
            <h2>{card.title}</h2>
            <p>{card.text}</p>
          </Link>
        ))}
      </section>

      <section className="card example-card" aria-label="Пример прогноза">
        <h2>82 балла, B057, МУИТ</h2>
        <p>Прогноз с погрешностью показывает, где шанс сильнее и какие источники стоит открыть перед заявкой.</p>
      </section>
    </main>
  );
}
