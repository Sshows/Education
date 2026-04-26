'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { FeatureLock } from '../../../components/FeatureLock';
import { DEMO_PROGRAM_GROUPS, getSubjectCombinationByPair, type SubjectId } from '../../../lib/ent-subjects';
import { DISCLAIMER_TEMPLATE } from '../../../../../packages/shared/src/constants';

const DEMO_UNIVERSITIES: Record<string, { name: string; city: string }> = {
  iitu: { name: 'МУИТ / IITU', city: 'Алматы' },
  aitu: { name: 'Astana IT University', city: 'Астана' },
  kbtu: { name: 'KBTU', city: 'Алматы' },
  sdu: { name: 'SDU University', city: 'Каскелен' },
  kaznu: { name: 'КазНУ аль-Фараби', city: 'Алматы' },
};

function ResultContent() {
  const params = useSearchParams();
  const scoreParam = params.get('score') ?? '82';
  const programCode = params.get('program') ?? 'B057';
  const comboParam = params.get('combo') ?? 'informatics+mathematics';

  const score = parseInt(scoreParam, 10);

  // Resolve combo
  const [s1, s2] = comboParam.split('+') as [SubjectId, SubjectId];
  const combo = getSubjectCombinationByPair(s1, s2);

  // Demo program
  const pg = DEMO_PROGRAM_GROUPS.find((p) => p.code === programCode) ?? DEMO_PROGRAM_GROUPS[0];

  // Demo thresholds (replace with real API data when available)
  const historicalCutoff = 78;
  const grantMinScore = 75;
  const paidMinScore = 50;
  const errorMargin = 9;
  const confidence = 'medium';

  const grantEligible = score >= grantMinScore;
  const paidEligible = score >= paidMinScore;
  const margin = score - historicalCutoff;
  const probability = !grantEligible
    ? 0
    : Math.min(99, Math.max(1, Math.round(50 + (margin / 15) * 40)));

  const cutoffPct = Math.min(100, Math.round((historicalCutoff / 140) * 100));
  const scorePct = Math.min(100, Math.round((score / 140) * 100));

  const disclaimer = DISCLAIMER_TEMPLATE.replace('{error_margin}', String(errorMargin));

  const confidenceLabel: Record<string, string> = {
    high: 'Высокая',
    medium: 'Средняя',
    low: 'Низкая',
  };

  return (
    <main>
      <p className="eyebrow">Результат</p>
      <h1 className="page-title">
        {probability >= 60 ? 'Шанс выше среднего' : probability >= 30 ? 'Умеренный шанс' : 'Низкий шанс'}
      </h1>
      <p className="page-subtitle">
        Демо-прогноз для <strong>{programCode}</strong>.{' '}
        <span className="demo-badge">Демо-данные</span>
      </p>

      {/* Hero: probability ring + metrics */}
      <section className="result-hero" aria-label="Основные метрики">
        {/* Probability ring */}
        <div
          className="probability-ring"
          style={{ '--value': probability } as React.CSSProperties}
          role="img"
          aria-label={`Вероятность гранта: ${probability}%`}
        >
          <div className="probability-ring__inner">
            <strong>{probability}%</strong>
            <span>шанс гранта</span>
          </div>
        </div>

        {/* Metrics column */}
        <div className="grid" style={{ gap: 8 }}>
          <div className="metric card" style={{ border: '1px solid var(--glass-border)' }}>
            <span className="small">Ваш балл</span>
            <strong style={{ color: 'var(--teal)' }}>{score}</strong>
          </div>
          <div className="metric card" style={{ border: '1px solid var(--glass-border)' }}>
            <span className="small">Ориентир прошлого конкурса</span>
            <strong>{historicalCutoff}</strong>
          </div>
          <div className="metric card" style={{ border: '1px solid var(--glass-border)' }}>
            <span className="small">Разница</span>
            <strong style={{ color: margin >= 0 ? 'var(--success)' : 'var(--danger)' }}>
              {margin >= 0 ? '+' : ''}{margin}
            </strong>
          </div>
        </div>
      </section>

      {/* Score comparison bar */}
      <section className="card" style={{ marginTop: 12 }} aria-label="Сравнение балла">
        <h2>Балл vs исторический cutoff</h2>

        <div className="score-bar-wrap" style={{ marginTop: 12 }}>
          <div className="score-bar-label">
            <span>Ваш балл: {score}</span>
            <span>140</span>
          </div>
          <div className="score-bar">
            <span className="score-bar__user" style={{ width: `${scorePct}%` }} />
            <span className="score-bar__cutoff" style={{ left: `${cutoffPct}%` }} />
          </div>
          <div className="score-bar-label">
            <span>0</span>
            <span style={{ color: 'var(--warning)' }}>▲ Cutoff: {historicalCutoff}</span>
          </div>
        </div>

        <p className="small" style={{ marginTop: 8 }}>
          {margin >= 0
            ? `Ваш балл выше исторического cutoff на ${margin} пунктов.`
            : `Ваш балл ниже исторического cutoff на ${Math.abs(margin)} пунктов.`}
          {' '}Оценочная погрешность: ±{errorMargin} п.п.
        </p>
      </section>

      {/* Subject & program info */}
      <section className="card" style={{ marginTop: 10 }} aria-label="Профиль">
        <h2>Профиль</h2>
        <div className="program-card__meta" style={{ marginTop: 10 }}>
          {combo && (
            <span className="tag">📚 {combo.label.ru}</span>
          )}
          <span className="tag">📋 {pg.code} — {pg.name.ru}</span>
          <span className="tag">🏛 {pg.category}</span>
          <span className="demo-badge">Демо-данные</span>
        </div>
      </section>

      {/* Eligibility */}
      <section className="card" style={{ marginTop: 10 }} aria-label="Право на участие">
        <h2>Право на участие</h2>
        <div className="program-card__meta" style={{ marginTop: 10 }}>
          <span
            className={grantEligible ? 'official-badge' : 'demo-badge'}
            style={{ background: grantEligible ? undefined : 'rgba(244,63,94,0.12)', color: grantEligible ? undefined : 'var(--danger)' }}
          >
            {grantEligible ? '✓ Грант' : '✗ Грант недоступен'}
          </span>
          <span
            className={paidEligible ? 'official-badge' : 'demo-badge'}
            style={{ background: paidEligible ? undefined : 'rgba(244,63,94,0.12)', color: paidEligible ? undefined : 'var(--danger)' }}
          >
            {paidEligible ? '✓ Платное' : '✗ Платное недоступно'}
          </span>
        </div>
        {!grantEligible && (
          <p className="small" style={{ marginTop: 8, color: 'var(--danger)' }}>
            Минимальный балл для гранта: {grantMinScore}. Ваш балл {score} ниже порога.
          </p>
        )}
      </section>

      {/* Confidence */}
      <section className="card" style={{ marginTop: 10 }} aria-label="Достоверность">
        <h2>Достоверность прогноза</h2>
        <div style={{ marginTop: 8 }}>
          <span className="confidence-badge">{confidenceLabel[confidence] ?? confidence}</span>
        </div>
        <p className="small" style={{ marginTop: 8 }}>
          Прогноз основан на исторических данных. При нехватке официальных данных
          погрешность возрастает.
        </p>
      </section>

      <FeatureLock
        title="Разблокировать полный прогноз"
        text="Premium покажет расширенные рекомендации, разбор источников, comparison по вузам и PDF-отчёт."
      />

      {/* Reason cards */}
      <section className="card" style={{ marginTop: 10 }}>
        <h2>Почему такой результат</h2>
        <div className="grid" style={{ gap: 8, marginTop: 10 }}>
          {margin < 0 && (
            <div className="card warning" style={{ padding: '10px 14px' }}>
              <p className="small" style={{ margin: 0 }}>
                ⚠ Ваш балл ниже исторического проходного на {Math.abs(margin)} пунктов.
              </p>
            </div>
          )}
          {margin >= 0 && margin < 5 && (
            <div className="card warning" style={{ padding: '10px 14px' }}>
              <p className="small" style={{ margin: 0 }}>
                ⚠ Разница минимальна ({margin} п.) — конкуренция высокая.
              </p>
            </div>
          )}
          {paidEligible && !grantEligible && (
            <div className="card" style={{ padding: '10px 14px', borderColor: 'rgba(79,124,255,0.3)' }}>
              <p className="small" style={{ margin: 0 }}>
                ℹ Вы проходите минимальный порог на платное обучение.
              </p>
            </div>
          )}
          <div className="card" style={{ padding: '10px 14px' }}>
            <p className="small" style={{ margin: 0 }}>
              ℹ Данные демонстрационные — подключите API для официального расчёта.
            </p>
          </div>
        </div>
      </section>

      {/* Recommendations */}
      <section className="card" style={{ marginTop: 10 }} aria-label="Рекомендации">
        <h2>Похожие программы</h2>
        <div className="grid" style={{ gap: 8, marginTop: 10 }}>
          {DEMO_PROGRAM_GROUPS.filter((p) => p.subjectPairKey === pg.subjectPairKey && p.code !== pg.code)
            .slice(0, 3)
            .map((p) => (
              <div key={p.code} className="program-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong style={{ fontSize: 14 }}>{p.code}</strong>
                  <p style={{ fontSize: 13, margin: '2px 0 0', color: 'var(--muted)' }}>{p.name.ru}</p>
                </div>
                <span className="demo-badge">Демо</span>
              </div>
            ))}
        </div>
      </section>

      {/* Sources */}
      <section className="card" style={{ marginTop: 10 }} aria-label="Источники">
        <h2>Источники</h2>
        <div className="program-card__meta" style={{ marginTop: 8 }}>
          <span className="source-badge">НЦТ</span>
          <span className="source-badge">МНВО РК</span>
          <span className="source-badge">Приёмные комиссии</span>
        </div>
        <p className="small" style={{ marginTop: 8 }}>
          Данные из открытых публикаций НЦТ и МНВО. Используйте как ориентир
          и проверяйте в официальных источниках вуза.
        </p>
      </section>

      {/* Disclaimer */}
      <section className="disclaimer" style={{ marginTop: 12 }} aria-label="Дисклеймер">
        <p>{disclaimer}</p>
      </section>
    </main>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={
      <main>
        <div className="skeleton skeleton-title" style={{ marginTop: 20 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 12 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 10 }} />
      </main>
    }>
      <ResultContent />
    </Suspense>
  );
}
