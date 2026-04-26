'use client';

import { useMemo, useState } from 'react';

import { UniversityCard } from '../../components/UniversityCard';
import { universities } from '../../lib/demo-data';

const cities = ['Все', 'Алматы', 'Астана', 'Каскелен'];

export default function UniversitiesPage() {
  const [query, setQuery] = useState('');
  const [city, setCity] = useState('Все');

  const visibleUniversities = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return universities.filter((university) => {
      const matchesQuery = `${university.name} ${university.city} ${university.focus}`.toLowerCase().includes(normalized);
      const matchesCity = city === 'Все' || university.city === city;
      return matchesQuery && matchesCity;
    });
  }, [city, query]);

  return (
    <main>
      <p className="eyebrow">Каталог</p>
      <h1 className="page-title">Вузы</h1>
      <p className="page-subtitle">Список для первичного выбора: город, профиль и ориентир прошлых конкурсов.</p>

      <input className="search-input" placeholder="Поиск по вузу, городу или профилю" value={query} onChange={(event) => setQuery(event.target.value)} />

      <div className="chips" aria-label="Фильтры городов">
        {cities.map((item) => (
          <button className={city === item ? 'chip chip--active' : 'chip'} key={item} onClick={() => setCity(item)}>
            {item}
          </button>
        ))}
      </div>

      <section className="catalog-grid">
        {visibleUniversities.map((university) => (
          <UniversityCard key={university.id} university={university} />
        ))}
      </section>
    </main>
  );
}
