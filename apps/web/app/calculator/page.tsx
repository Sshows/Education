import Link from 'next/link';

export default function CalculatorPage() {
  return (
    <main>
      <h2>Калькулятор ЕНТ</h2>
      <div className="card">MVP: форма ввода баллов, предметов, квот, региона и цели поступления.</div>
      <Link className="button" href="/result/1">Показать демо-результат</Link>
    </main>
  );
}
