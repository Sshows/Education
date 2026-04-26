'use client';

import { useCallback, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

import { SUBJECT_COMBINATIONS, DEMO_PROGRAM_GROUPS } from '../../lib/ent-subjects';
import { useTelegram } from '../../hooks/useTelegram';

const CATEGORIES = ['Все', 'IT', 'Инженерия', 'Медицина', 'Бизнес', 'Педагогика', 'Право', 'Языки'];

const CATEGORY_FILTER: Record<string, string[]> = {
  IT: ['B057', 'B058', 'B059', 'B157'],
  Инженерия: ['B062', 'B063', 'B064', 'B065', 'B071', 'B074'],
  Медицина: ['B084', 'B085', 'B086', 'B087', 'B088'],
  Бизнес: ['B044', 'B045', 'B046', 'B047'],
  Педагогика: ['B001', 'B002', 'B003'],
  Право: ['B049'],
  Языки: ['B018', 'B036', 'B037'],
};

function ProgramsContent() {
  const params = useSearchParams();
  const { hapticSelect } = useTelegram();

  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('Все');

  // combo param from URL (e.g. from Home quick-links or calculator)
  const comboParam = params.get('combo');
  const [selectedCombo, setSelectedCombo] = useState<string | null>(comboParam);

  const programs = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return DEMO_PROGRAM_GROUPS.filter((p) => {
      const matchQuery = normalized
        ? `${p.code} ${p.name.ru} ${p.name.en} ${p.subjectPairKey}`.toLowerCase().includes(normalized)
        : true;

      const matchCategory =
        category === 'Все' || (CATEGORY_FILTER[category]?.includes(p.code) ?? false);

      const matchCombo = selectedCombo ? p.subjectPairKey === selectedCombo : true;

      return matchQuery && matchCategory && matchCombo;
    });
  }, [query, category, selectedCombo]);

  const handleCategory = useCallback((cat: string) => {
    hapticSelect();
    setCategory(cat);
  }, [hapticSelect]);

  const handleComboFilter = useCallback((key: string) => {
    hapticSelect();
    setSelectedCombo((prev) => (prev === key ? null : key));
  }, [hapticSelect]);

  return (
    <main>
      <p className="eyebrow">Каталог</p>
      <h1 className="page-title">Программы ЕНТ</h1>
      <p className="page-subtitle">
        Группы образовательных программ с предметными парами.{' '}
        <span className="demo-badge">Демо-данные</span>
      </p>

      {/* Search */}
      <div className="field" style={{ marginTop: 12 }}>
        <input
          aria-label="Поиск программ"
          className="search-input"
          placeholder="Поиск по коду, названию, предметам..."
          style={{ width: '100%', minHeight: 48 }}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {/* Category chips */}
      <div className="chips" aria-label="Фильтры категорий" style={{ marginTop: 10 }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={category === cat ? 'chip chip--active' : 'chip'}
            type="button"
            onClick={() => handleCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Combo filter */}
      <div className="chips" aria-label="Фильтр по парам предметов" style={{ marginTop: 6 }}>
        <span className="small" style={{ alignSelf: 'center', marginRight: 4 }}>Предметы:</span>
        {SUBJECT_COMBINATIONS.slice(0, 6).map((combo) => {
          const isActive = selectedCombo === combo.key;
          return (
            <button
              key={combo.key}
              className={isActive ? 'chip chip--active' : 'chip'}
              style={{ fontSize: 12 }}
              type="button"
              onClick={() => handleComboFilter(combo.key)}
            >
              {combo.aliases[0] ?? combo.label.ru.split(' + ')[0]}
            </button>
          );
        })}
        {selectedCombo && (
          <button className="chip" style={{ fontSize: 12 }} type="button" onClick={() => setSelectedCombo(null)}>
            ✕ Сбросить
          </button>
        )}
      </div>

      {/* Active combo info */}
      {selectedCombo && (
        (() => {
          const combo = SUBJECT_COMBINATIONS.find((c) => c.key === selectedCombo);
          return combo ? (
            <div className="card example-card" style={{ marginTop: 10, padding: '12px 14px' }}>
              <strong style={{ fontSize: 14 }}>{combo.label.ru}</strong>
              <p className="small" style={{ margin: '4px 0 0' }}>{combo.category.ru}</p>
              <div className="program-card__meta" style={{ marginTop: 8 }}>
                {combo.aliases.slice(0, 3).map((a) => (
                  <span key={a} className="tag">{a}</span>
                ))}
              </div>
            </div>
          ) : null;
        })()
      )}

      {/* Results */}
      <p className="small" style={{ marginTop: 12, marginBottom: 6 }}>
        Найдено: <strong>{programs.length}</strong> программ
      </p>

      <section className="catalog-grid" aria-label="Программы">
        {programs.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state__icon">🔍</div>
            <p>Программы не найдены по этим фильтрам</p>
            <button
              className="secondary-button"
              type="button"
              onClick={() => { setQuery(''); setCategory('Все'); setSelectedCombo(null); }}
            >
              Сбросить фильтры
            </button>
          </div>
        ) : (
          programs.map((prog) => {
            const combo = SUBJECT_COMBINATIONS.find((c) => c.key === prog.subjectPairKey);
            return (
              <article key={prog.code} className="program-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <code style={{ fontSize: 13, color: 'var(--accent)', letterSpacing: '0.05em' }}>{prog.code}</code>
                    <h2 style={{ marginTop: 4, fontSize: 15 }}>{prog.name.ru}</h2>
                    <p style={{ fontSize: 13, color: 'var(--muted)', marginTop: 4 }}>{prog.name.en}</p>
                  </div>
                  <span className="demo-badge" style={{ flexShrink: 0 }}>Демо</span>
                </div>

                <div className="program-card__meta">
                  {combo && (
                    <span className="tag" style={{ fontSize: 11 }}>
                      📚 {combo.aliases[0] ?? combo.label.ru}
                    </span>
                  )}
                  <span className="tag" style={{ fontSize: 11 }}>🏷 {prog.category}</span>
                </div>
              </article>
            );
          })
        )}
      </section>
    </main>
  );
}

export default function ProgramsPage() {
  return (
    <Suspense fallback={
      <main>
        <div className="skeleton skeleton-title" style={{ marginTop: 20 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 12 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 10 }} />
        <div className="skeleton skeleton-card" style={{ marginTop: 10 }} />
      </main>
    }>
      <ProgramsContent />
    </Suspense>
  );
}
