import './styles.css';
import { ReactNode } from 'react';

import { TelegramProvider } from '../components/TelegramProvider';

export const metadata = {
  title: 'ENT Grant',
  description: 'Telegram Mini App для оценки шансов поступления по ЕНТ',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <TelegramProvider>{children}</TelegramProvider>
      </body>
    </html>
  );
}
