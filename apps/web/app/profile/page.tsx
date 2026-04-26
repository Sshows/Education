'use client';

import Link from 'next/link';

import { useTelegramContext } from '../../context/TelegramContext';
import { useTelegram } from '../../hooks/useTelegram';

export default function ProfilePage() {
  const { user, isInsideTelegram, platform, colorScheme, authStatus } = useTelegramContext();
  const { hapticImpact, openTelegramLink } = useTelegram();

  const avatarLetter = user?.first_name?.[0] ?? '?';
  const displayName = user ? `${user.first_name}${user.last_name ? ` ${user.last_name}` : ''}` : 'Гость';
  const handle = user?.username ? `@${user.username}` : null;

  return (
    <main>
      <p className="eyebrow">Профиль</p>
      <h1 className="page-title">Мой профиль</h1>

      {/* Telegram User Card */}
      <section className="card" style={{ marginTop: 16 }}>
        {isInsideTelegram && user ? (
          <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
            {/* Avatar */}
            <div
              style={{
                width: 56,
                height: 56,
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #4f7cff 0%, #00d4aa 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 22,
                fontWeight: 800,
                color: '#fff',
                flexShrink: 0,
              }}
              aria-hidden="true"
            >
              {avatarLetter}
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 17 }}>{displayName}</div>
              {handle && <div style={{ color: 'var(--muted)', fontSize: 13 }}>{handle}</div>}
              {user.language_code && (
                <div style={{ marginTop: 4, display: 'flex', gap: 6 }}>
                  <span className="tag">{user.language_code.toUpperCase()}</span>
                  {user.is_premium && <span className="official-badge">⭐ Premium</span>}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="empty-state" style={{ padding: '20px 0' }}>
            <div className="empty-state__icon">👤</div>
            <p>Откройте в Telegram для персонализации</p>
            <Link
              className="secondary-button"
              href={`https://t.me/${process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? 'entgrant_kz_bot'}`}
              style={{ fontSize: 13 }}
            >
              Открыть бота
            </Link>
          </div>
        )}
      </section>

      {/* Auth status */}
      {isInsideTelegram && (
        <div style={{ marginTop: 8, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {authStatus === 'ok' && <span className="official-badge">✓ Авторизован</span>}
          {authStatus === 'loading' && <span className="confidence-badge">⟳ Авторизация...</span>}
          {authStatus === 'error' && <span className="demo-badge">✗ Ошибка авторизации</span>}
          <span className="source-badge">📱 {platform}</span>
          <span className="source-badge">{colorScheme === 'dark' ? '🌙 Тёмная' : '☀️ Светлая'}</span>
        </div>
      )}

      {/* Stats */}
      <section className="grid grid--two" style={{ gap: 8, marginTop: 12 }}>
        <div className="metric card" style={{ border: '1px solid var(--glass-border)' }}>
          <span className="small">Расчётов</span>
          <strong>0</strong>
          <span className="hint" style={{ fontSize: 11 }}>Нет истории</span>
        </div>
        <div className="metric card" style={{ border: '1px solid var(--glass-border)' }}>
          <span className="small">Цель</span>
          <strong style={{ fontSize: 18 }}>B057</strong>
          <span className="hint" style={{ fontSize: 11 }}>Demo-данные</span>
        </div>
      </section>

      {/* Actions */}
      <section className="card" style={{ marginTop: 12 }}>
        <h2>Действия</h2>
        <div className="grid" style={{ gap: 8, marginTop: 12 }}>
          <Link
            className="button"
            href="/calculator"
            onClick={() => hapticImpact('light')}
            style={{ justifyContent: 'flex-start', gap: 10 }}
          >
            🎯 Новый расчёт
          </Link>
          <Link
            className="secondary-button"
            href="/profile/billing"
            style={{ justifyContent: 'flex-start', gap: 10 }}
          >
            💳 Платежи и доступ
          </Link>
          <Link
            className="secondary-button"
            href="/pricing"
            onClick={() => hapticImpact('light')}
            style={{ justifyContent: 'flex-start', gap: 10 }}
          >
            ⭐ Premium-тарифы
          </Link>
          <Link
            className="ghost-button"
            href="/support"
            style={{ justifyContent: 'flex-start', gap: 10 }}
          >
            💬 Поддержка
          </Link>
        </div>
      </section>

      {/* Links */}
      <section className="card" style={{ marginTop: 10 }}>
        <h2>Документы</h2>
        <div className="grid" style={{ gap: 6, marginTop: 10 }}>
          <Link className="ghost-button" href="/terms" style={{ justifyContent: 'flex-start', fontSize: 13 }}>
            📄 Условия использования
          </Link>
          <Link className="ghost-button" href="/privacy" style={{ justifyContent: 'flex-start', fontSize: 13 }}>
            🔒 Политика конфиденциальности
          </Link>
          <Link className="ghost-button" href="/refund-policy" style={{ justifyContent: 'flex-start', fontSize: 13 }}>
            💰 Политика возврата
          </Link>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="disclaimer" style={{ marginTop: 12 }}>
        <p>
          Данные профиля — из Telegram initData. Backend верифицирует подпись самостоятельно.
          Никакие личные данные не хранятся без вашего ведома.
        </p>
      </section>
    </main>
  );
}
