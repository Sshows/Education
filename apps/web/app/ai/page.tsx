import { FeatureLock } from '../../components/FeatureLock';

export default function AIPage() {
  return (
    <main>
      <p className="eyebrow">AI-консультант</p>
      <h1 className="page-title">Спросить AI</h1>
      <p className="page-subtitle">Ответы должны опираться на источники; если данных нет, интерфейс честно скажет об этом.</p>

      <section className="card">
        <h2>Вопрос</h2>
        <p>Подойдёт ли B057 при 82 баллах и математике с информатикой?</p>
      </section>
      <section className="card">
        <h2>Ответ</h2>
        <p>Для демо-профиля стоит проверить МУИТ, Astana IT и SDU. Подтверждённых свежих данных по итоговому конкурсу пока нет.</p>
      </section>
      <FeatureLock
        title="AI-кредиты закончились"
        text="Купите AI-пакет или Premium, чтобы задавать вопросы по источникам и сохранять ответы."
      />
    </main>
  );
}
