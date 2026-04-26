'use client';

import { useMemo, useState } from 'react';

import { ProgramCard } from '../../components/ProgramCard';
import { programs } from '../../lib/demo-data';

const filters = ['Все', 'IT', 'Безопасность', 'Инженерия'];

export default function ProgramsPage() {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('Все');

  const visiblePrograms = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return programs.filter((program) => {
      const matchesQuery = `${program.code} ${program.name} ${program.subjects}`.toLowerCase().includes(normalized);
      const matchesFilter =
        filter === 'Все' ||
        (filter === 'IT' && program.code !== 'B157') ||
        (filter === 'Безопасность' && program.code === 'B058') ||
        (filter === 'Инженерия' && program.code === 'B157');
      return matchesQuery && matchesFilter;
    });
  }, [filter, query]);

  return (
    <main>
      <p className="eyebrow">Каталог</p>
      <h1 className="page-title">Программы</h1>
      <p className="page-subtitle">Демо-данные помогают выбрать направление, пока API или импорт источников недоступны.</p>

      <input className="search-input" placeholder="Поиск по коду, названию или предметам" value={query} onChange={(event) => setQuery(event.target.value)} />

      <div className="chips" aria-label="Фильтры программ">
        {filters.map((item) => (
          <button className={filter === item ? 'chip chip--active' : 'chip'} key={item} onClick={() => setFilter(item)}>
            {item}
          </button>
        ))}
      </div>

      <section className="catalog-grid">
        {visiblePrograms.map((program) => (
          <ProgramCard key={program.code} program={program} />
        ))}
      </section>
    </main>
  );
}
