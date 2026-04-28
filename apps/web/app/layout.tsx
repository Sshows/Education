import './styles.css';
import type { Metadata, Viewport } from 'next';
import { ReactNode } from 'react';

import { TelegramProvider } from '../components/TelegramProvider';

export const metadata: Metadata = {
  title: {
    default: 'ГрантМетр — шанс на грант по ЕНТ',
    template: '%s | ГрантМетр',
  },
  description:
    'Telegram Mini App для расчёта шанса на грант по ЕНТ: балл, предметы, квота и специальности.',
  keywords: ['ЕНТ', 'грант', 'поступление', 'Казахстан', 'калькулятор', 'МНВО', 'НЦТ'],
  openGraph: {
    title: 'ГрантМетр — шанс на грант по ЕНТ',
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
