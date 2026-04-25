'use client';

import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AdminPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [conflicts, setConflicts] = useState<any[]>([]);

  async function load() {
    try {
      const [s, c] = await Promise.all([
        fetch(`${API}/api/admin/sources`).then((r) => r.json()),
        fetch(`${API}/api/admin/conflicts`).then((r) => r.json()),
      ]);
      setSources(s);
      setConflicts(c.items || []);
    } catch {
      setSources([]);
      setConflicts([]);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <main>
      <h2>Admin</h2>
      <div className="card">
        <h3>Sources</h3>
        <ul>
          {sources.map((s) => (
            <li key={s.id}>
              {s.title} — {s.status} — {s.fetched_at || 'not fetched'}
              <div>
                <button className="button" onClick={() => fetch(`${API}/api/admin/sources/${s.id}/fetch`, { method: 'POST' }).then(() => load())}>fetch</button>
                <button className="button" onClick={() => fetch(`${API}/api/admin/sources/${s.id}/parse`, { method: 'POST' }).then(() => load())}>parse</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h3>Conflicts</h3>
        <ul>
          {conflicts.map((c, idx) => <li key={idx}>{c.message}</li>)}
          {conflicts.length === 0 && <li>Нет конфликтов</li>}
        </ul>
      </div>
    </main>
  );
}
