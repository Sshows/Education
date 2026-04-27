'use client';

import { getTelegramWebApp, isTelegramWebApp } from './telegram';

export type PaymentProduct = {
  code: string;
  title_ru: string;
  description_ru?: string;
  product_type: string;
  stars_price?: number;
  kzt_price?: number;
  currency: string;
  features: string[];
  is_active: boolean;
};

export const fallbackProducts: PaymentProduct[] = [
  {
    code: 'free',
    title_ru: 'Бесплатно',
    description_ru: 'Базовый калькулятор, каталог программ и вузов.',
    product_type: 'one_time',
    stars_price: 0,
    kzt_price: 0,
    currency: 'XTR',
    features: ['basic_calculator', 'catalog'],
    is_active: true,
  },
  {
    code: 'pro_once',
    title_ru: 'Полный прогноз',
    description_ru: 'Расширенный прогноз, рекомендации, источники и score vs cutoff.',
    product_type: 'one_time',
    stars_price: 50,
    kzt_price: 490,
    currency: 'XTR',
    features: ['full_forecast', 'recommendations', 'source_breakdown'],
    is_active: true,
  },
  {
    code: 'ai_pack',
    title_ru: 'AI-пакет',
    description_ru: '20 вопросов AI-консультанту.',
    product_type: 'consumable',
    stars_price: 100,
    kzt_price: 990,
    currency: 'XTR',
    features: ['ai_questions_20'],
    is_active: true,
  },
  {
    code: 'premium_month',
    title_ru: 'Premium на месяц',
    description_ru: 'Безлимитные прогнозы, 100 AI-вопросов, профиль и алерты.',
    product_type: 'subscription',
    stars_price: 250,
    kzt_price: 1990,
    currency: 'XTR',
    features: ['unlimited_forecasts', 'ai_questions_100', 'saved_profile', 'alerts'],
    is_active: true,
  },
];

export function botDeepLink(action: string): string {
  const username = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME || 'entgrant_kz_bot';
  return `https://t.me/${username}?start=${action}`;
}

export function startStarsPurchase(productCode: string): void {
  getTelegramWebApp()?.HapticFeedback?.impactOccurred?.('medium');
  window.location.href = botDeepLink(`buy_${productCode}`);
}

export function isAipayCheckoutEnabled(): boolean {
  return process.env.NEXT_PUBLIC_PAYMENTS_ENABLE_AIPAY === 'true';
}

export async function startAipayCheckout(productCode: string): Promise<void> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    throw new Error('API URL is not configured');
  }
  const response = await fetch(`${apiUrl}/api/payment/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_code: productCode,
      provider: 'aipay',
      return_url: `${window.location.origin}/payment/success`,
    }),
  });
  if (!response.ok) {
    throw new Error(`Payment API ${response.status}`);
  }
  const data = await response.json() as { payment_url?: string; checkout_url?: string };
  const checkoutUrl = data.payment_url ?? data.checkout_url;
  if (!checkoutUrl) {
    throw new Error('Payment URL is missing');
  }
  window.location.href = checkoutUrl;
}

export async function fetchProducts(): Promise<PaymentProduct[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    return fallbackProducts;
  }
  try {
    const response = await fetch(`${apiUrl}/api/payments/products`, { cache: 'no-store' });
    if (!response.ok) {
      return fallbackProducts;
    }
    return response.json();
  } catch {
    return fallbackProducts;
  }
}

export function paymentContextLabel(): string {
  return isTelegramWebApp()
    ? 'В Telegram для цифрового доступа используется Stars.'
    : 'Оплата Stars доступна через бота. Карта / Kaspi / Freedom включаются только после настройки провайдера.';
}
