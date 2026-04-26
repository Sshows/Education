import Link from 'next/link';

export default function ProfilePage() {
  return (
    <main>
      <p className="eyebrow">Профиль</p>
      <h1 className="page-title">Мой профиль</h1>
      <p className="page-subtitle">Telegram-профиль появляется после backend validation через initData.</p>

      <section className="grid">
        <div className="metric">
          <span className="small">Расчётов</span>
          <strong>0</strong>
        </div>
        <div className="metric">
          <span className="small">Сохранённая цель</span>
          <strong>B057</strong>
        </div>
        <Link className="button" href="/calculator">Новый расчёт</Link>
        <Link className="ghost-button" href="/profile/billing">Платежи и доступ</Link>
        <Link className="secondary-button" href="/pricing">Premium</Link>
      </section>
    </main>
  );
}
