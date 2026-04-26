export default function SupportPage() {
  return (
    <main>
      <p className="eyebrow">Support</p>
      <h1 className="page-title">Поддержка</h1>
      <section className="card">
        <h2>Проблема с оплатой</h2>
        <p>Укажите order id, продукт, дату оплаты и провайдер. Не отправляйте данные карты или секреты.</p>
      </section>
      <section className="card">
        <h2>В боте</h2>
        <p>Используйте команды /restore и /support.</p>
      </section>
    </main>
  );
}
