import type { ReactNode } from 'react';

import { FeatureLock } from './FeatureLock';

export function PremiumGate({ unlocked, children }: { unlocked?: boolean; children: ReactNode }) {
  if (unlocked) {
    return <>{children}</>;
  }
  return (
    <FeatureLock
      title="Детальный разбор доступен в Premium"
      text="Откройте рекомендации, источники, объяснение confidence и сравнение нескольких вузов."
    />
  );
}
