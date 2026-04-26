'use client';

// ============================================================
// Telegram Mini App SDK — Full type coverage
// Based on: https://core.telegram.org/bots/webapps
// Pattern from: https://github.com/softstack/telegram-mini-app
// ============================================================

export type TelegramThemeParams = {
  bg_color?: string;
  text_color?: string;
  hint_color?: string;
  link_color?: string;
  button_color?: string;
  button_text_color?: string;
  secondary_bg_color?: string;
  header_bg_color?: string;
  bottom_bar_bg_color?: string;
  accent_text_color?: string;
  section_bg_color?: string;
  section_header_text_color?: string;
  subtitle_text_color?: string;
  destructive_text_color?: string;
};

export type HapticFeedbackStyle = 'light' | 'medium' | 'heavy' | 'rigid' | 'soft';
export type HapticNotificationType = 'error' | 'success' | 'warning';

export type TelegramHapticFeedback = {
  impactOccurred: (style: HapticFeedbackStyle) => void;
  notificationOccurred: (type: HapticNotificationType) => void;
  selectionChanged: () => void;
};

export type TelegramMainButton = {
  text: string;
  color: string;
  textColor: string;
  isVisible: boolean;
  isActive: boolean;
  isProgressVisible: boolean;
  show: () => void;
  hide: () => void;
  enable: () => void;
  disable: () => void;
  showProgress: (leaveActive?: boolean) => void;
  hideProgress: () => void;
  setText: (text: string) => void;
  setParams: (params: {
    text?: string;
    color?: string;
    text_color?: string;
    is_active?: boolean;
    is_visible?: boolean;
  }) => void;
  onClick: (callback: () => void) => void;
  offClick: (callback: () => void) => void;
};

export type TelegramBackButton = {
  isVisible: boolean;
  show: () => void;
  hide: () => void;
  onClick: (callback: () => void) => void;
  offClick: (callback: () => void) => void;
};

export type TelegramSettingsButton = {
  isVisible: boolean;
  show: () => void;
  hide: () => void;
  onClick: (callback: () => void) => void;
  offClick: (callback: () => void) => void;
};

export type TelegramCloudStorage = {
  setItem: (key: string, value: string, callback?: (error: Error | null, stored: boolean) => void) => void;
  getItem: (key: string, callback: (error: Error | null, value: string) => void) => void;
  getItems: (keys: string[], callback: (error: Error | null, values: Record<string, string>) => void) => void;
  removeItem: (key: string, callback?: (error: Error | null, removed: boolean) => void) => void;
  removeItems: (keys: string[], callback?: (error: Error | null, removed: boolean) => void) => void;
  getKeys: (callback: (error: Error | null, keys: string[]) => void) => void;
};

export type TelegramPopupButton = {
  id?: string;
  type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive';
  text?: string;
};

export type TelegramPopupParams = {
  title?: string;
  message: string;
  buttons?: TelegramPopupButton[];
};

export type TelegramScanQrPopupParams = {
  text?: string;
};

export type TelegramInvoiceStatus = 'paid' | 'cancelled' | 'failed' | 'pending';

export type TelegramViewport = {
  height: number;
  width: number;
  stableHeight: number;
  isExpanded: boolean;
};

export type TelegramUser = {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium?: boolean;
  photo_url?: string;
  allows_write_to_pm?: boolean;
};

export type TelegramInitDataUnsafe = {
  user?: TelegramUser;
  receiver?: TelegramUser;
  chat?: { id: number; type: string; title: string; username?: string };
  start_param?: string;
  auth_date?: number;
  hash?: string;
};

export type TelegramPlatform =
  | 'android'
  | 'android_x'
  | 'ios'
  | 'macos'
  | 'tdesktop'
  | 'weba'
  | 'webk'
  | 'unigram'
  | 'unknown';

export type TelegramWebApp = {
  // Core
  initData: string;
  initDataUnsafe: TelegramInitDataUnsafe;
  version: string;
  platform: TelegramPlatform;
  colorScheme: 'light' | 'dark';
  themeParams: TelegramThemeParams;
  isExpanded: boolean;
  viewportHeight: number;
  viewportStableHeight: number;
  headerColor: string;
  backgroundColor: string;
  bottomBarColor: string;
  isClosingConfirmationEnabled: boolean;
  isVerticalSwipesEnabled: boolean;

  // Lifecycle
  ready: () => void;
  expand: () => void;
  close: () => void;

  // Events
  onEvent: (eventType: string, eventHandler: (...args: unknown[]) => void) => void;
  offEvent: (eventType: string, eventHandler: (...args: unknown[]) => void) => void;
  sendData: (data: string) => void;

  // UI controls
  MainButton: TelegramMainButton;
  BackButton: TelegramBackButton;
  SettingsButton: TelegramSettingsButton;
  HapticFeedback: TelegramHapticFeedback;
  CloudStorage: TelegramCloudStorage;

  // Popups
  showPopup: (params: TelegramPopupParams, callback?: (buttonId: string) => void) => void;
  showAlert: (message: string, callback?: () => void) => void;
  showConfirm: (message: string, callback?: (confirmed: boolean) => void) => void;
  showScanQrPopup: (params: TelegramScanQrPopupParams, callback?: (text: string) => boolean) => void;
  closeScanQrPopup: () => void;

  // Payments
  openInvoice: (url: string, callback?: (status: TelegramInvoiceStatus) => void) => void;

  // Navigation
  openLink: (url: string, options?: { try_instant_view?: boolean }) => void;
  openTelegramLink: (url: string) => void;
  switchInlineQuery: (query: string, choose_chat_types?: string[]) => void;

  // Colors
  setHeaderColor: (color: string) => void;
  setBackgroundColor: (color: string) => void;
  setBottomBarColor: (color: string) => void;

  // Misc
  enableClosingConfirmation: () => void;
  disableClosingConfirmation: () => void;
  enableVerticalSwipes: () => void;
  disableVerticalSwipes: () => void;
  requestWriteAccess: (callback?: (access: boolean) => void) => void;
  requestContact: (callback?: (contact: boolean) => void) => void;
  isVersionAtLeast: (version: string) => boolean;
  readTextFromClipboard: (callback?: (text: string) => void) => void;
};

// Global window augmentation
declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
}

// ============================================================
// Core access functions
// ============================================================

export function getTelegramWebApp(): TelegramWebApp | null {
  if (typeof window === 'undefined') return null;
  return window.Telegram?.WebApp ?? null;
}

export function isTelegramWebApp(): boolean {
  const webApp = getTelegramWebApp();
  return Boolean(webApp?.initData);
}

export function getTelegramUser(): TelegramUser | null {
  return getTelegramWebApp()?.initDataUnsafe?.user ?? null;
}

export function getTelegramPlatform(): TelegramPlatform {
  return getTelegramWebApp()?.platform ?? 'unknown';
}

export function isMobilePlatform(): boolean {
  const platform = getTelegramPlatform();
  return platform === 'android' || platform === 'android_x' || platform === 'ios';
}

// ============================================================
// Theme
// ============================================================

export function applyTelegramTheme(webApp: TelegramWebApp | null = getTelegramWebApp()): void {
  if (typeof document === 'undefined' || !webApp) return;

  const root = document.documentElement;
  const theme = webApp.themeParams ?? {};

  const setVar = (name: string, value?: string) => {
    if (value) root.style.setProperty(name, value);
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

// ============================================================
// Haptics helpers
// ============================================================

export const haptic = {
  impact(style: HapticFeedbackStyle = 'medium') {
    getTelegramWebApp()?.HapticFeedback?.impactOccurred(style);
  },
  notification(type: HapticNotificationType) {
    getTelegramWebApp()?.HapticFeedback?.notificationOccurred(type);
  },
  selection() {
    getTelegramWebApp()?.HapticFeedback?.selectionChanged();
  },
};

// ============================================================
// Cloud Storage helpers (Promise wrappers)
// ============================================================

export function cloudSet(key: string, value: string): Promise<boolean> {
  return new Promise((resolve) => {
    const cs = getTelegramWebApp()?.CloudStorage;
    if (!cs) return resolve(false);
    cs.setItem(key, value, (err, stored) => resolve(!err && stored));
  });
}

export function cloudGet(key: string): Promise<string | null> {
  return new Promise((resolve) => {
    const cs = getTelegramWebApp()?.CloudStorage;
    if (!cs) return resolve(null);
    cs.getItem(key, (err, value) => resolve(err ? null : value));
  });
}

export function cloudGetAll(keys: string[]): Promise<Record<string, string>> {
  return new Promise((resolve) => {
    const cs = getTelegramWebApp()?.CloudStorage;
    if (!cs) return resolve({});
    cs.getItems(keys, (err, values) => resolve(err ? {} : values));
  });
}

// ============================================================
// Telegram auth
// ============================================================

export async function authTelegram(): Promise<{
  ok: boolean;
  status: 'telegram' | 'development' | 'browser' | 'unavailable';
}> {
  const webApp = getTelegramWebApp();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? '';
  const endpoint = `${apiUrl}/api/auth/telegram`;

  if (webApp?.initData) {
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData: webApp.initData }),
      });
      return { ok: res.ok, status: 'telegram' };
    } catch {
      return { ok: false, status: 'unavailable' };
    }
  }

  if (process.env.NODE_ENV === 'development') {
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      return { ok: res.ok, status: 'development' };
    } catch {
      return { ok: false, status: 'unavailable' };
    }
  }

  return { ok: false, status: 'browser' };
}

// ============================================================
// Invoice (Stars)
// ============================================================

export function openTelegramInvoice(
  invoiceLink: string,
  onDone?: (status: TelegramInvoiceStatus) => void,
): void {
  const webApp = getTelegramWebApp();
  if (webApp?.openInvoice) {
    webApp.openInvoice(invoiceLink, onDone);
  } else {
    // fallback: open in browser
    window.open(invoiceLink, '_blank');
  }
}
