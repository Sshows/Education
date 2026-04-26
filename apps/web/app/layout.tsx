import './styles.css';
import type { Metadata, Viewport } from 'next';
import { ReactNode } from 'react';

import { TelegramProvider } from '../components/TelegramProvider';

export const metadata: Metadata = {
  title: {
    default: 'ENT Grant KZ — Шанс поступления по ЕНТ',
    template: '%s | ENT Grant KZ',
  },
  description:
    'Рассчитай шанс поступления на грант или платное по результатам ЕНТ. Калькулятор с историческими данными, вузами Казахстана и программами ОП.',
  keywords: ['ЕНТ', 'грант', 'поступление', 'Казахстан', 'калькулятор', 'МНВО', 'НЦТ'],
  openGraph: {
    title: 'ENT Grant KZ — Шанс поступления по ЕНТ',
    description: 'Ориентировочный прогноз поступления по открытым данным НЦТ и МНВО.',
    type: 'website',
    locale: 'ru_KZ',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: '#0f1523',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <head>
        {/* Telegram Mini App SDK */}
        <script src="https://telegram.org/js/telegram-web-app.js" />
      </head>
      <body>
        <TelegramProvider>{children}</TelegramProvider>
      </body>
    </html>
  );
}
