'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useTelegram } from '../../hooks/useTelegram';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: number;
};

const SUGGESTED = [
  'Какой минимальный балл для B057 в МУИТ?',
  'Чем отличается грантовое от платного обучения?',
  'Когда подавать документы на поступление?',
  'Что такое квота "сельская местность"?',
  'Как работает конкурс грантов?',
];

const DISCLAIMER =
  'AI-консультант предоставляет ориентировочную информацию по открытым данным. ' +
  'Проверяйте актуальные условия в официальных источниках (НЦТ, МНВО, приёмных комиссиях вузов).';

type ApiMessage = {
  role: 'user' | 'assistant';
  content: string;
};

async function fetchAiReply(messages: ApiMessage[]): Promise<string> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
  const res = await fetch(`${apiUrl}/api/ai/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });
  if (!res.ok) {
    throw new Error(`AI API ${res.status}`);
  }
  const data = (await res.json()) as { reply?: string; message?: string };
  return data.reply ?? data.message ?? 'Нет ответа от сервера.';
}

export default function AiPage() {
  const { hapticImpact, hapticNotify, showMainButton, hideMainButton } = useTelegram();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    hapticImpact('light');
    setInput('');
    setError(null);

    const userMsg: Message = {
      id: `u-${Date.now()}`,
      role: 'user',
      text: trimmed,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    const history: ApiMessage[] = [...messages, userMsg].slice(-10).map((m) => ({
      role: m.role,
      content: m.text,
    }));

    try {
      const reply = await fetchAiReply(history);
      const assistantMsg: Message = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        text: reply,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      hapticNotify('success');
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Ошибка сети';
      setError(msg);
      hapticNotify('error');
    } finally {
      setLoading(false);
    }
  }, [loading, messages, hapticImpact, hapticNotify]);

  // MainButton = Send (when input not empty)
  useEffect(() => {
    if (input.trim()) {
      showMainButton('Отправить', () => { void sendMessage(input); });
    } else {
      hideMainButton();
    }
    return () => hideMainButton();
  }, [input, sendMessage, showMainButton, hideMainButton]);

  return (
    <main style={{ display: 'flex', flexDirection: 'column', minHeight: '85dvh' }}>
      <p className="eyebrow">AI-консультант</p>
      <h1 className="page-title">Спроси про ЕНТ</h1>

      {/* Disclaimer */}
      <div className="demo-badge" style={{ alignSelf: 'flex-start', marginTop: 8, marginBottom: 12 }}>
        ⚠ Только ориентировочно — проверяйте официально
      </div>

      {/* Suggested questions (shown when no messages) */}
      {messages.length === 0 && (
        <section aria-label="Популярные вопросы">
          <p className="small" style={{ marginBottom: 8 }}>Популярные вопросы:</p>
          <div className="grid" style={{ gap: 6 }}>
            {SUGGESTED.map((q) => (
              <button
                key={q}
                className="secondary-button"
                style={{ textAlign: 'left', justifyContent: 'flex-start', fontSize: 13, minHeight: 40 }}
                onClick={() => { void sendMessage(q); }}
                type="button"
              >
                {q}
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Chat messages */}
      <section
        aria-label="Диалог"
        style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 10, marginTop: 12 }}
      >
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '85%',
              padding: '10px 14px',
              borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
              background: msg.role === 'user'
                ? 'linear-gradient(135deg, #4f7cff 0%, #7c4fff 100%)'
                : 'var(--surface-2)',
              border: '1px solid var(--glass-border)',
              fontSize: 14,
              lineHeight: 1.5,
              color: msg.role === 'user' ? '#fff' : 'var(--ink)',
            }}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div
            style={{
              alignSelf: 'flex-start',
              background: 'var(--surface-2)',
              border: '1px solid var(--glass-border)',
              borderRadius: '18px 18px 18px 4px',
              padding: '10px 16px',
            }}
          >
            <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  style={{
                    width: 6,
                    height: 6,
                    borderRadius: '50%',
                    background: 'var(--muted)',
                    animation: `bounce 1.2s ${i * 0.2}s ease-in-out infinite`,
                  }}
                />
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mismatch-warning" style={{ alignSelf: 'flex-start' }}>
            <strong>⚠ Ошибка:</strong> {error}
          </div>
        )}

        <div ref={bottomRef} />
      </section>

      {/* Input */}
      <div
        className="sticky-action"
        style={{ position: 'sticky', bottom: 'calc(80px + env(safe-area-inset-bottom, 0px))' }}
      >
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            aria-label="Сообщение"
            className="search-input"
            disabled={loading}
            placeholder="Задайте вопрос про ЕНТ..."
            style={{ flex: 1, minHeight: 48 }}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                void sendMessage(input);
              }
            }}
          />
          <button
            aria-label="Отправить"
            className="button"
            disabled={loading || !input.trim()}
            style={{ minWidth: 48, padding: '0 14px' }}
            type="button"
            onClick={() => { void sendMessage(input); }}
          >
            ↑
          </button>
        </div>
        <p className="small" style={{ textAlign: 'center', marginTop: 6 }}>
          {DISCLAIMER}
        </p>
      </div>

      {/* Bounce animation */}
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </main>
  );
}
