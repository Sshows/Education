'use client';

import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';

import { BottomNav } from './BottomNav';
import { applyTelegramTheme, authTelegram, getTelegramWebApp, isTelegramWebApp } from '../lib/telegram';

const BOT_USERNAME = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? 'entgrant_kz_bot';

export function TelegramProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [insideTelegram, setInsideTelegram] = useState(true); // optimistic: assume inside

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const isTg = isTelegramWebApp();
    setInsideTelegram(isTg);

    if (!webApp) return;

    webApp.ready();
    webApp.expand();
    applyTelegramTheme(webApp);
    void authTelegram();
  }, []);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const backButton = webApp?.BackButton;
    if (!backButton) return;

    const goBack = () => {
      if (pathname === '/') {
        router.push('/');
      } else {
        router.back();
      }
    };

    if (pathname === '/') {
      backButton.hide();
    } else {
      backButton.show();
      webApp?.onEvent?.('backButtonClicked', goBack);
    }

    return () => {
      webApp?.offEvent?.('backButtonClicked', goBack);
    };
  }, [pathname, router]);

  return (
    <>
      {!insideTelegram && (
        <div className="telegram-banner">
          <span>Откройте через Telegram для полного опыта</span>
          <a href={`https://t.me/${BOT_USERNAME}`} rel="noopener noreferrer" target="_blank">
            Открыть @{BOT_USERNAME} →
          </a>
        </div>
      )}
      <div className="app-shell">
        {children}
        <BottomNav />
      </div>
    </>
  );
}
