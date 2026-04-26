'use client';

// ============================================================
// useBackButton — Manages Telegram BackButton for a page
// Usage: call at page top level, pass shouldShow and onBack
// ============================================================

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { getTelegramWebApp } from '../lib/telegram';

type Options = {
  /** Show the back button? Default: true */
  show?: boolean;
  /** Custom back handler. Default: router.back() */
  onBack?: () => void;
};

export function useBackButton({ show = true, onBack }: Options = {}) {
  const router = useRouter();
  const handlerRef = useRef<() => void>(() => router.back());

  useEffect(() => {
    handlerRef.current = onBack ?? (() => router.back());
  }, [onBack, router]);

  useEffect(() => {
    const webApp = getTelegramWebApp();
    const btn = webApp?.BackButton;
    if (!btn) return;

    const handler = () => handlerRef.current();

    if (show) {
      btn.show();
      btn.onClick(handler);
    } else {
      btn.hide();
    }

    return () => {
      btn.offClick(handler);
      btn.hide();
    };
  }, [show]);
}
