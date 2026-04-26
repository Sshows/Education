'use client';

export type TelegramThemeParams = {
  bg_color?: string;
  text_color?: string;
  hint_color?: string;
  link_color?: string;
  button_color?: string;
  button_text_color?: string;
  secondary_bg_color?: string;
};

type TelegramButton = {
  show: () => void;
  hide: () => void;
  setText?: (text: string) => void;
  setParams?: (params: { text?: string; color?: string; text_color?: string; is_active?: boolean }) => void;
  enable?: () => void;
  disable?: () => void;
};

export type TelegramWebApp = {
  initData: string;
  initDataUnsafe?: { user?: Record<string, unknown> };
  colorScheme?: 'light' | 'dark';
  themeParams?: TelegramThemeParams;
  BackButton?: TelegramButton;
  MainButton?: TelegramButton;
  HapticFeedback?: {
    impactOccurred?: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
    notificationOccurred?: (type: 'error' | 'success' | 'warning') => void;
  };
  ready: () => void;
  expand: () => void;
  onEvent?: (eventType: string, eventHandler: () => void) => void;
  offEvent?: (eventType: string, eventHandler: () => void) => void;
};

declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
}

export function getTelegramWebApp(): TelegramWebApp | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return window.Telegram?.WebApp ?? null;
}

export function isTelegramWebApp(): boolean {
  return Boolean(getTelegramWebApp()?.initData);
}

export function applyTelegramTheme(webApp: TelegramWebApp | null = getTelegramWebApp()): void {
  if (typeof document === 'undefined' || !webApp) {
    return;
  }

  const root = document.documentElement;
  const theme = webApp.themeParams ?? {};
  const setVar = (name: string, value?: string) => {
    if (value) {
      root.style.setProperty(name, value);
    }
  };

  setVar('--tg-bg-color', theme.bg_color);
  setVar('--tg-text-color', theme.text_color);
  setVar('--tg-hint-color', theme.hint_color);
  setVar('--tg-link-color', theme.link_color);
  setVar('--tg-button-color', theme.button_color);
  setVar('--tg-button-text-color', theme.button_text_color);
  setVar('--tg-secondary-bg-color', theme.secondary_bg_color);
  root.dataset.telegramTheme = webApp.colorScheme ?? 'light';
}

export async function authTelegram(): Promise<{ ok: boolean; status: 'telegram' | 'development' | 'browser' | 'unavailable' }> {
  const webApp = getTelegramWebApp();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
  const endpoint = `${apiUrl}/api/auth/telegram`;

  if (webApp?.initData) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData: webApp.initData }),
      });
      return { ok: response.ok, status: 'telegram' };
    } catch {
      return { ok: false, status: 'unavailable' };
    }
  }

  if (process.env.NODE_ENV === 'development') {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      return { ok: response.ok, status: 'development' };
    } catch {
      return { ok: false, status: 'unavailable' };
    }
  }

  return { ok: false, status: 'browser' };
}
