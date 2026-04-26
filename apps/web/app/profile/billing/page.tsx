import Link from 'next/link';

export default function BillingPage() {
  return (
    <main>
      <p className="eyebrow">Billing</p>
      <h1 className="page-title">Платежи и доступ</h1>
      <p className="page-subtitle">Здесь отображаются продукт, статус, провайдер, дата и order id после подключения API.</p>
      <section className="card">
        <h2>Активный доступ</h2>
        <p>Откройте Mini App через Telegram, чтобы восстановить доступ по Telegram ID.</p>
      </section>
      <section className="card">
        <h2>Нужна помощь?</h2>
        <p>Если оплата прошла, но доступ не появился, нажмите /restore в боте или откройте поддержку.</p>
      </section>
      <Link className="button" href="/support">Поддержка</Link>
    </main>
  );
}
