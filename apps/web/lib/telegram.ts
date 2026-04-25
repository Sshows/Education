'use client';

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData?: string;
        ready: () => void;
        expand: () => void;
        BackButton: { show: () => void; hide: () => void; onClick: (fn: () => void) => void };
        MainButton: { show: () => void; hide: () => void; setText: (text: string) => void; onClick: (fn: () => void) => void };
      };
    };
  }
}

export function initTelegramWebApp() {
  const app = window.Telegram?.WebApp;
  if (!app) return null;
  app.ready();
  app.expand();
  return app;
}
