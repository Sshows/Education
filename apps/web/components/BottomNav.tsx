'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', label: 'Главная', icon: '🏠' },
  { href: '/calculator', label: 'Расчёт', icon: '🎯' },
  { href: '/programs', label: 'Программы', icon: '📋' },
  { href: '/universities', label: 'Вузы', icon: '🏛' },
  { href: '/profile', label: 'Профиль', icon: '👤' },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="bottom-nav" aria-label="Основная навигация">
      {navItems.map((item) => {
        const active = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
        return (
          <Link
            className={active ? 'bottom-nav__item bottom-nav__item--active' : 'bottom-nav__item'}
            href={item.href}
            key={item.href}
            aria-current={active ? 'page' : undefined}
          >
            <span className="bottom-nav__icon" aria-hidden="true">{item.icon}</span>
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
