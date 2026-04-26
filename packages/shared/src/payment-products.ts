export const PAYMENT_PRODUCTS = [
  {
    code: 'free',
    titleRu: 'Бесплатно',
    productType: 'one_time',
    starsPrice: 0,
    kztPrice: 0,
    features: ['basic_calculator', 'catalog'],
  },
  {
    code: 'pro_once',
    titleRu: 'Полный прогноз',
    productType: 'one_time',
    starsPrice: 50,
    kztPrice: 490,
    features: ['full_forecast', 'recommendations', 'source_breakdown'],
  },
  {
    code: 'ai_pack',
    titleRu: 'AI-пакет',
    productType: 'consumable',
    starsPrice: 100,
    kztPrice: 990,
    features: ['ai_questions_20'],
  },
  {
    code: 'premium_month',
    titleRu: 'Premium на месяц',
    productType: 'subscription',
    starsPrice: 250,
    kztPrice: 1990,
    features: ['unlimited_forecasts', 'ai_questions_100', 'saved_profile', 'alerts'],
  },
] as const;
