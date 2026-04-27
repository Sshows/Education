'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import { useTelegram } from '../hooks/useTelegram';
import {
  fallbackProducts,
  fetchProducts,
  isAipayCheckoutEnabled,
  paymentContextLabel,
  startAipayCheckout,
  startStarsPurchase,
  type PaymentProduct,
} from '../lib/payments';

const FEATURE_LABELS: Record<string, string> = {
  basic_calculator: '🎯 Базовый калькулятор',
  catalog: '📋 Каталог программ и вузов',
  full_forecast: '📊 Полный прогноз',
  recommendations: '💡 Рекомендации',
  source_breakdown: '🔍 Разбор источников',
  ai_questions_20: '🤖 20 AI-вопросов',
  unlimited_forecasts: '♾ Безлимитные прогнозы',
  ai_questions_100: '🤖 100 AI-вопросов',
  saved_profile: '👤 Сохранённый профиль',
  alerts: '📅 Алерты по дедлайнам',
};

export function PricingClient() {
  const { hapticImpact, hapticNotify, isInsideTelegram } = useTelegram();
  const [products, setProducts] = useState<PaymentProduct[]>(fallbackProducts);
  const [purchasing, setPurchasing] = useState<string | null>(null);
  const [externalPurchasing, setExternalPurchasing] = useState<string | null>(null);

  useEffect(() => {
    void fetchProducts().then(setProducts);
  }, []);

  const handleBuy = async (productCode: string) => {
    hapticImpact('medium');
    setPurchasing(productCode);
    try {
      await startStarsPurchase(productCode);
      hapticNotify('success');
    } catch {
      hapticNotify('error');
    } finally {
      setPurchasing(null);
    }
  };

  const handleAipay = async (productCode: string) => {
    hapticImpact('medium');
    setExternalPurchasing(productCode);
    try {
      await startAipayCheckout(productCode);
    } catch {
      hapticNotify('error');
      setExternalPurchasing(null);
    }
  };

  return (
    <main>
      <p className="eyebrow">Premium</p>
      <h1 className="page-title">Оплата через Telegram Stars ⭐</h1>
      <p className="page-subtitle">{paymentContextLabel()}</p>

      {!isInsideTelegram && (
        <div className="card warning" style={{ marginTop: 12, padding: '12px 16px' }} role="alert">
          <strong style={{ color: 'var(--warning)' }}>⚠ Откройте в Telegram</strong>
          <p className="small" style={{ margin: '4px 0 0' }}>
            Оплата Stars доступна только внутри Telegram Mini App.
          </p>
        </div>
      )}

      {/* Product cards */}
      <section
        style={{ display: 'grid', gap: 12, marginTop: 16 }}
        aria-label="Тарифы"
      >
        {products.map((product) => {
          const isPaid = product.code !== 'free';
          const isBuying = purchasing === product.code;
          return (
            <article
              key={product.code}
              className={isPaid ? 'card example-card' : 'card'}
              style={{ padding: '18px 16px', position: 'relative' }}
            >
              {/* Badge */}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
                <span className={isPaid ? 'official-badge' : 'tag'}>{product.product_type}</span>
                {isPaid && <span className="confidence-badge">⭐ {product.stars_price} Stars</span>}
              </div>

              <h2 style={{ margin: 0 }}>{product.title_ru}</h2>
              <p className="small" style={{ marginTop: 6 }}>{product.description_ru}</p>

              {/* Price */}
              {isPaid && (
                <div style={{ marginTop: 12, display: 'flex', alignItems: 'baseline', gap: 8 }}>
                  <strong style={{ fontSize: 22, color: 'var(--teal)' }}>
                    ⭐ {product.stars_price}
                  </strong>
                  <span className="small">≈ {product.kzt_price} ₸</span>
                </div>
              )}

              {/* Features */}
              <ul style={{ margin: '12px 0 0', padding: 0, listStyle: 'none', display: 'grid', gap: 6 }}>
                {product.features.map((feature) => (
                  <li key={feature} style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ color: 'var(--success)' }}>✓</span>
                    {FEATURE_LABELS[feature] ?? feature}
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <div style={{ marginTop: 16, display: 'grid', gap: 8 }}>
                {isPaid ? (
                  <>
                    <button
                      className="button"
                      disabled={isBuying || !isInsideTelegram}
                      style={{ width: '100%' }}
                      type="button"
                      onClick={() => { void handleBuy(product.code); }}
                    >
                      {isBuying ? '⟳ Открытие...' : `💫 Оплатить ${product.stars_price} Stars`}
                    </button>
                    {isAipayCheckoutEnabled() ? (
                      <button
                        className="ghost-button"
                        disabled={externalPurchasing === product.code}
                        style={{ width: '100%', fontSize: 13 }}
                        type="button"
                        onClick={() => { void handleAipay(product.code); }}
                      >
                        {externalPurchasing === product.code ? 'Открываем checkout...' : 'Карта через AiPay'}
                      </button>
                    ) : (
                      <button className="ghost-button" disabled style={{ width: '100%', fontSize: 13 }} type="button">
                        Карта / Kaspi / Freedom — включается после настройки
                      </button>
                    )}
                  </>
                ) : (
                  <Link className="secondary-button" href="/calculator" style={{ width: '100%', justifyContent: 'center' }}>
                    Начать бесплатно →
                  </Link>
                )}
              </div>
            </article>
          );
        })}
      </section>

      {/* Trust section */}
      <section className="card" style={{ marginTop: 16, padding: '16px' }}>
        <h2>🔒 Безопасность оплаты</h2>
        <ul style={{ margin: '10px 0 0', padding: 0, listStyle: 'none', display: 'grid', gap: 8, fontSize: 13 }}>
          <li>✓ Оплата проходит через официальный Telegram Payments API</li>
          <li>✓ Доступ активируется только после подтверждения платежа</li>
          <li>✓ Мы не храним данные карт и приватные ключи</li>
          <li>✓ Stars возвращаются согласно политике возврата Telegram</li>
        </ul>
        <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <Link className="ghost-button" href="/refund-policy" style={{ fontSize: 12, minHeight: 34 }}>
            Политика возврата
          </Link>
          <Link className="ghost-button" href="/terms" style={{ fontSize: 12, minHeight: 34 }}>
            Условия
          </Link>
          <Link className="ghost-button" href="/support" style={{ fontSize: 12, minHeight: 34 }}>
            Поддержка
          </Link>
        </div>
      </section>
    </main>
  );
}
