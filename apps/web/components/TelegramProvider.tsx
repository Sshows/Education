'use client';

import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';

import { BottomNav } from './BottomNav';
import { applyTelegramTheme, authTelegram, getTelegramWebApp, isTelegramWebApp } from '../lib/telegram';

export function TelegramProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [insideTelegram, setInsideTelegram] = useState(true);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    setInsideTelegram(isTelegramWebApp());

    if (!webApp) {
      return;
    }

    webApp.ready();
    webApp.expand();
    applyTelegramTheme(webApp);
    void authTelegram();
  }, []);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const backButton = webApp?.BackButton;
    if (!backButton) {
      return;
    }

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
      {!insideTelegram ? <div className="telegram-banner">Откройте через Telegram для полного опыта</div> : null}
      <div className="app-shell">
        {children}
        <BottomNav />
      </div>
    </>
  );
}
