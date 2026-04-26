import Link from 'next/link';

export default function PaymentCancelPage() {
  return (
    <main>
      <p className="eyebrow">Оплата</p>
      <h1 className="page-title">Оплата не завершена</h1>
      <p className="page-subtitle">Заказ можно создать заново. Доступ не активируется без подтверждения провайдера.</p>
      <section className="card payment-state">
        <h2>Статус: canceled</h2>
        <p>Деньги не должны списаться, если Telegram или внешний checkout отменил оплату.</p>
      </section>
      <Link className="button" href="/pricing">Вернуться к тарифам</Link>
    </main>
  );
}
