'use client';

import { useEffect, useState } from 'react';

import { fallbackProducts, fetchProducts, paymentContextLabel, startStarsPurchase, type PaymentProduct } from '../lib/payments';

const featureLabels: Record<string, string> = {
  basic_calculator: 'Базовый калькулятор',
  catalog: 'Каталог программ и вузов',
  full_forecast: 'Полный прогноз',
  recommendations: 'Рекомендации',
  source_breakdown: 'Разбор источников',
  ai_questions_20: '20 AI-вопросов',
  unlimited_forecasts: 'Безлимитные прогнозы',
  ai_questions_100: '100 AI-вопросов',
  saved_profile: 'Сохранённый профиль',
  alerts: 'Алерты по дедлайнам',
};

export function PricingClient() {
  const [products, setProducts] = useState<PaymentProduct[]>(fallbackProducts);

  useEffect(() => {
    void fetchProducts().then(setProducts);
  }, []);

  return (
    <main>
      <p className="eyebrow">Premium</p>
      <h1 className="page-title">Оплата внутри Telegram — Stars</h1>
      <p className="page-subtitle">{paymentContextLabel()}</p>

      <section className="pricing-grid">
        {products.map((product) => {
          const paid = product.code !== 'free';
          return (
            <article className={paid ? 'pricing-card pricing-card--paid' : 'pricing-card'} key={product.code}>
              <div>
                <span className="tag">{product.product_type}</span>
                <h2>{product.title_ru}</h2>
                <p>{product.description_ru}</p>
              </div>
              <div className="price-line">
                <strong>{product.stars_price ?? 0} Stars</strong>
                <span>≈ {product.kzt_price ?? 0} KZT</span>
              </div>
              <ul className="feature-list">
                {product.features.map((feature) => (
                  <li key={feature}>{featureLabels[feature] ?? feature}</li>
                ))}
              </ul>
              {paid ? (
                <>
                  <button className="button" onClick={() => startStarsPurchase(product.code)}>Оплатить Stars</button>
                  <button className="ghost-button" disabled>Карта / Kaspi / Freedom</button>
                </>
              ) : (
                <span className="small">Доступно без оплаты.</span>
              )}
            </article>
          );
        })}
      </section>

      <section className="card trust-card">
        <h2>Безопасность оплаты</h2>
        <p>Доступ активируется только после подтверждения платежа провайдером. Мы не храним данные карт и приватные ключи.</p>
      </section>
    </main>
  );
}
