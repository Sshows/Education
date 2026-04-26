'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', label: 'Главная' },
  { href: '/calculator', label: 'Расчёт' },
  { href: '/programs', label: 'Программы' },
  { href: '/universities', label: 'Вузы' },
  { href: '/profile', label: 'Профиль' },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="bottom-nav" aria-label="Основная навигация">
      {navItems.map((item) => {
        const active = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
        return (
          <Link className={active ? 'bottom-nav__item bottom-nav__item--active' : 'bottom-nav__item'} href={item.href} key={item.href}>
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
