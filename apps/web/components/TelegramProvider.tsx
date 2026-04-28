'use client';

import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';

import { BottomNav } from './BottomNav';
import { TelegramContextProvider, useTelegramContext } from '../context/TelegramContext';
import { getTelegramWebApp } from '../lib/telegram';

const BOT_USERNAME = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? 'entgrant_kz_bot';

// ---- Inner shell ---- (has access to context)
function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { isInsideTelegram } = useTelegramContext();
  const immersiveFlow = pathname === '/' || pathname.startsWith('/calculator') || pathname.startsWith('/result');

  // BackButton: show on all pages except home
  useEffect(() => {
    const webApp = getTelegramWebApp();
    const backButton = webApp?.BackButton;
    if (!backButton) return;

    const goBack = () => {
      if (pathname === '/') router.push('/');
      else router.back();
    };

    if (pathname === '/') {
      backButton.hide();
    } else {
      backButton.show();
      backButton.onClick(goBack);
    }

    return () => {
      backButton.offClick(goBack);
    };
  }, [pathname, router]);

  return (
    <>
      {!isInsideTelegram && (
        <div className="telegram-banner">
          <span>Откройте через Telegram для полного опыта</span>
          <a href={`https://t.me/${BOT_USERNAME}`} rel="noopener noreferrer" target="_blank">
            @{BOT_USERNAME} →
          </a>
        </div>
      )}
      <div className={immersiveFlow ? 'app-shell app-shell--immersive' : 'app-shell'}>
        {children}
        {!immersiveFlow && <BottomNav />}
      </div>
    </>
  );
}

// ---- Root provider ---- wraps context + shell
export function TelegramProvider({ children }: { children: React.ReactNode }) {
  return (
    <TelegramContextProvider>
      <AppShell>{children}</AppShell>
    </TelegramContextProvider>
  );
}
