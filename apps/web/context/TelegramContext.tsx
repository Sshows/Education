'use client';

// ============================================================
// TelegramContext — Global Telegram Mini App state
// Provides user, theme, platform info to all components
// ============================================================

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

import {
  applyTelegramTheme,
  authTelegram,
  getTelegramUser,
  getTelegramWebApp,
  isTelegramWebApp,
  type TelegramPlatform,
  type TelegramUser,
  type TelegramWebApp,
} from '../lib/telegram';

type TelegramContextValue = {
  webApp: TelegramWebApp | null;
  user: TelegramUser | null;
  isInsideTelegram: boolean;
  colorScheme: 'light' | 'dark';
  platform: TelegramPlatform;
  authStatus: 'idle' | 'loading' | 'ok' | 'error';
  startParam: string | null;
};

const TelegramContext = createContext<TelegramContextValue>({
  webApp: null,
  user: null,
  isInsideTelegram: false,
  colorScheme: 'dark',
  platform: 'unknown',
  authStatus: 'idle',
  startParam: null,
});

export function useTelegramContext(): TelegramContextValue {
  return useContext(TelegramContext);
}

export function TelegramContextProvider({ children }: { children: ReactNode }) {
  const [webApp] = useState<TelegramWebApp | null>(() => getTelegramWebApp());
  const [user] = useState<TelegramUser | null>(() => getTelegramUser());
  const [isInsideTelegram] = useState(() => isTelegramWebApp());
  const [colorScheme, setColorScheme] = useState<'light' | 'dark'>(() => webApp?.colorScheme ?? 'dark');
  const [platform] = useState<TelegramPlatform>(() => webApp?.platform ?? 'unknown');
  const [authStatus, setAuthStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle');
  const [startParam] = useState<string | null>(() => webApp?.initDataUnsafe?.start_param ?? null);

  // Initialize TMA
  useEffect(() => {
    if (!webApp) return;

    webApp.ready();
    webApp.expand();
    applyTelegramTheme(webApp);

    // Auth
    setAuthStatus('loading');
    void authTelegram().then((result) => {
      setAuthStatus(result.ok ? 'ok' : 'error');
    });
  }, [webApp]);

  // Listen for theme changes
  useEffect(() => {
    if (!webApp) return;

    const onThemeChanged = () => {
      setColorScheme(webApp.colorScheme ?? 'dark');
      applyTelegramTheme(webApp);
    };

    webApp.onEvent('themeChanged', onThemeChanged);
    return () => webApp.offEvent('themeChanged', onThemeChanged);
  }, [webApp]);

  return (
    <TelegramContext.Provider value={{ webApp, user, isInsideTelegram, colorScheme, platform, authStatus, startParam }}>
      {children}
    </TelegramContext.Provider>
  );
}
