'use client';

// ============================================================
// useTelegram hook — Central Telegram Mini App integration
// Inspired by: https://github.com/softstack/telegram-mini-app
// ============================================================

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import {
  applyTelegramTheme,
  cloudGet,
  cloudSet,
  getTelegramUser,
  getTelegramWebApp,
  haptic,
  isMobilePlatform,
  isTelegramWebApp,
  openTelegramInvoice,
  type HapticFeedbackStyle,
  type HapticNotificationType,
  type TelegramInvoiceStatus,
  type TelegramPlatform,
  type TelegramUser,
  type TelegramWebApp,
} from '../lib/telegram';

// ============================================================
// Types
// ============================================================

export type UseTelegramReturn = {
  // State
  webApp: TelegramWebApp | null;
  user: TelegramUser | null;
  isInsideTelegram: boolean;
  isMobile: boolean;
  platform: TelegramPlatform;
  colorScheme: 'light' | 'dark';
  viewportHeight: number;
  isExpanded: boolean;

  // Actions
  hapticImpact: (style?: HapticFeedbackStyle) => void;
  hapticNotify: (type: HapticNotificationType) => void;
  hapticSelect: () => void;
  expand: () => void;
  close: () => void;
  openLink: (url: string) => void;
  openTelegramLink: (url: string) => void;
  showAlert: (message: string) => void;
  showConfirm: (message: string) => Promise<boolean>;
  sendData: (data: string) => void;
  openInvoice: (url: string, onDone?: (status: TelegramInvoiceStatus) => void) => void;

  // MainButton
  showMainButton: (text: string, onClick: () => void, options?: { color?: string }) => void;
  hideMainButton: () => void;
  setMainButtonProgress: (show: boolean) => void;

  // Cloud Storage
  cloudGet: (key: string) => Promise<string | null>;
  cloudSet: (key: string, value: string) => Promise<boolean>;

  // Convenience
  startParam: string | null;
};

// ============================================================
// Hook
// ============================================================

export function useTelegram(): UseTelegramReturn {
  const [webApp] = useState<TelegramWebApp | null>(() =>
    typeof window !== 'undefined' ? getTelegramWebApp() : null
  );

  const [user] = useState<TelegramUser | null>(() =>
    typeof window !== 'undefined' ? getTelegramUser() : null
  );

  const [isInsideTelegram] = useState(() => isTelegramWebApp());
  const [isMobile] = useState(() => isMobilePlatform());
  const [platform] = useState<TelegramPlatform>(() => webApp?.platform ?? 'unknown');
  const [colorScheme, setColorScheme] = useState<'light' | 'dark'>(() => webApp?.colorScheme ?? 'dark');
  const [viewportHeight, setViewportHeight] = useState(() =>
    webApp?.viewportHeight ?? (typeof window !== 'undefined' ? window.innerHeight : 600)
  );
  const [isExpanded, setIsExpanded] = useState(() => webApp?.isExpanded ?? false);

  // Keep mainButton click ref to properly remove listeners
  const mainButtonClickRef = useRef<(() => void) | null>(null);

  // Initialize
  useEffect(() => {
    if (!webApp) return;
    webApp.ready();
    webApp.expand();
    applyTelegramTheme(webApp);
  }, [webApp]);

  // Listen for viewport changes
  useEffect(() => {
    if (!webApp) return;

    const onViewportChanged = () => {
      setViewportHeight(webApp.viewportHeight);
      setIsExpanded(webApp.isExpanded);
    };

    const onThemeChanged = () => {
      setColorScheme(webApp.colorScheme ?? 'dark');
      applyTelegramTheme(webApp);
    };

    webApp.onEvent('viewportChanged', onViewportChanged);
    webApp.onEvent('themeChanged', onThemeChanged);

    return () => {
      webApp.offEvent('viewportChanged', onViewportChanged);
      webApp.offEvent('themeChanged', onThemeChanged);
    };
  }, [webApp]);

  // ---- Actions ----

  const hapticImpact = useCallback((style: HapticFeedbackStyle = 'medium') => {
    haptic.impact(style);
  }, []);

  const hapticNotify = useCallback((type: HapticNotificationType) => {
    haptic.notification(type);
  }, []);

  const hapticSelect = useCallback(() => {
    haptic.selection();
  }, []);

  const expand = useCallback(() => {
    webApp?.expand();
  }, [webApp]);

  const close = useCallback(() => {
    webApp?.close();
  }, [webApp]);

  const openLink = useCallback((url: string) => {
    if (webApp?.openLink) {
      webApp.openLink(url);
    } else {
      window.open(url, '_blank');
    }
  }, [webApp]);

  const openTelegramLink = useCallback((url: string) => {
    if (webApp?.openTelegramLink) {
      webApp.openTelegramLink(url);
    } else {
      window.open(url, '_blank');
    }
  }, [webApp]);

  const showAlert = useCallback((message: string) => {
    if (webApp?.showAlert) {
      webApp.showAlert(message);
    } else {
      window.alert(message);
    }
  }, [webApp]);

  const showConfirm = useCallback((message: string): Promise<boolean> => {
    return new Promise((resolve) => {
      if (webApp?.showConfirm) {
        webApp.showConfirm(message, resolve);
      } else {
        resolve(window.confirm(message));
      }
    });
  }, [webApp]);

  const sendData = useCallback((data: string) => {
    webApp?.sendData(data);
  }, [webApp]);

  const openInvoice = useCallback((url: string, onDone?: (status: TelegramInvoiceStatus) => void) => {
    openTelegramInvoice(url, onDone);
  }, []);

  // ---- Main Button ----

  const showMainButton = useCallback((
    text: string,
    onClick: () => void,
    options?: { color?: string }
  ) => {
    const btn = webApp?.MainButton;
    if (!btn) return;

    // Remove previous listener
    if (mainButtonClickRef.current) {
      btn.offClick(mainButtonClickRef.current);
    }

    mainButtonClickRef.current = onClick;
    btn.setText(text);
    if (options?.color) {
      btn.setParams({ color: options.color });
    }
    btn.onClick(onClick);
    btn.enable();
    btn.show();
  }, [webApp]);

  const hideMainButton = useCallback(() => {
    const btn = webApp?.MainButton;
    if (!btn) return;
    if (mainButtonClickRef.current) {
      btn.offClick(mainButtonClickRef.current);
      mainButtonClickRef.current = null;
    }
    btn.hide();
  }, [webApp]);

  const setMainButtonProgress = useCallback((show: boolean) => {
    const btn = webApp?.MainButton;
    if (!btn) return;
    if (show) {
      btn.showProgress(false);
    } else {
      btn.hideProgress();
    }
  }, [webApp]);

  // ---- Convenience ----

  const startParam = useMemo(
    () => webApp?.initDataUnsafe?.start_param ?? null,
    [webApp]
  );

  return {
    webApp,
    user,
    isInsideTelegram,
    isMobile,
    platform,
    colorScheme,
    viewportHeight,
    isExpanded,
    hapticImpact,
    hapticNotify,
    hapticSelect,
    expand,
    close,
    openLink,
    openTelegramLink,
    showAlert,
    showConfirm,
    sendData,
    openInvoice,
    showMainButton,
    hideMainButton,
    setMainButtonProgress,
    cloudGet,
    cloudSet,
    startParam,
  };
}
