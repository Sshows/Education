import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Дедлайны поступления | ENT Grant KZ',
  description: 'Ключевые даты поступления 2025: ЕНТ, подача документов, зачисление, апелляции.',
};

type Deadline = {
  id: string;
  date: string;
  label: string;
  description: string;
  status: 'past' | 'upcoming' | 'critical';
  source?: string;
};

const DEADLINES_2025: Deadline[] = [
  {
    id: 'ent-reg',
    date: '1 апреля 2025',
    label: 'Регистрация на ЕНТ',
    description: 'Последний день регистрации для участия в ЕНТ-2025.',
    status: 'past',
    source: 'НЦТ',
  },
  {
    id: 'ent-main',
    date: 'Май–Июнь 2025',
    label: 'Основная сессия ЕНТ',
    description: 'Основная сессия единого национального тестирования. Даты уточняются НЦТ.',
    status: 'upcoming',
    source: 'НЦТ',
  },
  {
    id: 'results',
    date: 'Июль 2025',
    label: 'Результаты ЕНТ',
    description: 'Публикация официальных результатов и сертификатов.',
    status: 'upcoming',
    source: 'НЦТ',
  },
  {
    id: 'docs-submit',
    date: '25 июля 2025',
    label: 'Подача документов',
    description: 'Последний день подачи заявлений на грант через Портал поступающего.',
    status: 'critical',
    source: 'МНВО',
  },
  {
    id: 'quota',
    date: '28 июля 2025',
    label: 'Закрытие квот',
    description: 'Зачисление по сельской и социальной квоте.',
    status: 'critical',
    source: 'МНВО',
  },
  {
    id: 'grant-results',
    date: 'Август 2025',
    label: 'Объявление грантов',
    description: 'Публикация результатов конкурса грантов МНВО.',
    status: 'upcoming',
    source: 'МНВО',
  },
  {
    id: 'enrollment',
    date: '12–20 августа 2025',
    label: 'Зачисление',
    description: 'Приём оригиналов документов в вуз и приказ о зачислении.',
    status: 'upcoming',
    source: 'Вузы',
  },
  {
    id: 'appeal',
    date: '5 дней после результатов',
    label: 'Апелляция',
    description: 'Подача апелляции сразу после публикации результатов ЕНТ.',
    status: 'upcoming',
    source: 'НЦТ',
  },
];

const statusColor: Record<Deadline['status'], string> = {
  past: 'var(--muted)',
  upcoming: 'var(--accent)',
  critical: 'var(--danger)',
};

const statusLabel: Record<Deadline['status'], string> = {
  past: 'Прошёл',
  upcoming: 'Предстоит',
  critical: '⚠ Критично',
};

export default function DeadlinesPage() {
  return (
    <main>
      <p className="eyebrow">Поступление 2025</p>
      <h1 className="page-title">Дедлайны</h1>
      <p className="page-subtitle">
        Ориентировочные даты. Проверяйте актуальные сроки на сайтах{' '}
        <strong>НЦТ</strong> и <strong>МНВО</strong>.
      </p>

      {/* Critical banner */}
      <div
        className="card warning"
        style={{ marginTop: 12, padding: '12px 16px', display: 'flex', gap: 10, alignItems: 'flex-start' }}
        role="alert"
      >
        <span style={{ fontSize: 22 }}>⚠</span>
        <div>
          <strong style={{ display: 'block', color: 'var(--warning)' }}>Важно</strong>
          <p className="small" style={{ margin: '4px 0 0' }}>
            Даты проверены по открытым данным МНВО 2024 и могут отличаться для 2025 года.
            Всегда сверяйтесь с официальным сайтом.
          </p>
        </div>
      </div>

      {/* Timeline */}
      <section className="grid" style={{ gap: 8, marginTop: 16 }} aria-label="Дедлайны">
        {DEADLINES_2025.map((d) => (
          <article
            key={d.id}
            className="deadline-row"
            style={{
              padding: '14px 16px',
              display: 'block',
              borderLeft: `3px solid ${statusColor[d.status]}`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8 }}>
              <div>
                <strong style={{ fontSize: 15, display: 'block' }}>{d.label}</strong>
                <span
                  style={{ fontSize: 13, fontWeight: 700, color: statusColor[d.status], display: 'block', marginTop: 2 }}
                >
                  📅 {d.date}
                </span>
              </div>
              <div style={{ display: 'flex', gap: 4, flexShrink: 0 }}>
                <span
                  className="tag"
                  style={{ color: statusColor[d.status], borderColor: statusColor[d.status] + '44', background: statusColor[d.status] + '11' }}
                >
                  {statusLabel[d.status]}
                </span>
              </div>
            </div>
            <p className="small" style={{ margin: '8px 0 0' }}>{d.description}</p>
            {d.source && (
              <div style={{ marginTop: 8 }}>
                <span className="source-badge">📊 {d.source}</span>
              </div>
            )}
          </article>
        ))}
      </section>

      {/* Checklist */}
      <section className="card" style={{ marginTop: 12 }}>
        <h2>Что приготовить заранее</h2>
        <ul style={{ margin: '10px 0 0', paddingLeft: 22, lineHeight: 2, fontSize: 14 }}>
          <li>Сертификат ЕНТ (оригинал)</li>
          <li>Аттестат о среднем образовании</li>
          <li>Удостоверение личности (удостоверение/паспорт)</li>
          <li>Фото 3×4 (6 штук)</li>
          <li>Медицинская справка 086-У</li>
          <li>Документ о квоте (при наличии)</li>
          <li>Заявление (по форме вуза)</li>
        </ul>
      </section>

      {/* Links */}
      <section className="card" style={{ marginTop: 10 }}>
        <h2>Официальные источники</h2>
        <div className="grid" style={{ gap: 8, marginTop: 10 }}>
          <a
            className="secondary-button"
            href="https://testcenter.kz"
            rel="noopener noreferrer"
            style={{ justifyContent: 'flex-start', fontSize: 13 }}
            target="_blank"
          >
            🔗 НЦТ — testcenter.kz
          </a>
          <a
            className="secondary-button"
            href="https://talim.edu.kz"
            rel="noopener noreferrer"
            style={{ justifyContent: 'flex-start', fontSize: 13 }}
            target="_blank"
          >
            🔗 МНВО РК — talim.edu.kz
          </a>
          <a
            className="secondary-button"
            href="https://ent.cap.kz"
            rel="noopener noreferrer"
            style={{ justifyContent: 'flex-start', fontSize: 13 }}
            target="_blank"
          >
            🔗 Портал поступающего — ent.cap.kz
          </a>
        </div>
      </section>

      <Link className="button" href="/calculator" style={{ width: '100%', marginTop: 16, display: 'flex' }}>
        🎯 Рассчитать шанс на грант
      </Link>
    </main>
  );
}
