import Link from 'next/link';

export default function PaymentSuccessPage() {
  return (
    <main>
      <p className="eyebrow">Оплата</p>
      <h1 className="page-title">Доступ активирован</h1>
      <p className="page-subtitle">Если Premium не появился сразу, откройте профиль или нажмите /restore в боте.</p>
      <section className="card payment-state payment-state--success">
        <h2>Оплата прошла</h2>
        <p>Доступ активируется после подтверждения backend entitlement.</p>
      </section>
      <Link className="button" href="/result/demo">Открыть полный прогноз</Link>
    </main>
  );
}
