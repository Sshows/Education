'use client';

import { useEffect, useState } from 'react';

type Entitlement = {
  product_code: string;
  access_type: string;
  credits_total?: number;
  credits_used: number;
  is_active: boolean;
};

export function useEntitlements(telegramId?: number) {
  const [items, setItems] = useState<Entitlement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (!apiUrl || !telegramId) {
      setLoading(false);
      return;
    }
    const url = new URL(`${apiUrl}/api/payments/my-entitlements`);
    url.searchParams.set('telegram_id', String(telegramId));
    fetch(url)
      .then((response) => response.ok ? response.json() : [])
      .then(setItems)
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [telegramId]);

  return {
    items,
    loading,
    hasPremium: items.some((item) => item.is_active && item.product_code === 'premium_month'),
    hasPro: items.some((item) => item.is_active && ['pro_once', 'premium_month'].includes(item.product_code)),
  };
}
