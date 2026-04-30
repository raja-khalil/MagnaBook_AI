"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, LayoutDashboard, LogOut, PlusCircle } from "lucide-react";
import { clsx } from "clsx";
import { useAuthStore } from "@/store/auth";

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/projects/new", label: "Novo Projeto", icon: PlusCircle },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();

  return (
    <aside className="flex h-screen w-60 flex-col border-r border-gray-200 bg-white">
      <div className="flex items-center gap-2 px-5 py-5">
        <BookOpen className="text-brand-500" size={24} />
        <span className="text-lg font-bold text-gray-900">MagnaBook AI</span>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-2">
        {nav.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
              pathname.startsWith(href)
                ? "bg-brand-50 text-brand-600"
                : "text-gray-600 hover:bg-gray-100"
            )}
          >
            <Icon size={18} />
            {label}
          </Link>
        ))}
      </nav>

      <div className="border-t border-gray-100 px-3 py-3">
        <div className="mb-2 px-3 text-xs text-gray-400 truncate">{user?.email}</div>
        <button
          onClick={clearAuth}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-gray-600 hover:bg-gray-100"
        >
          <LogOut size={16} />
          Sair
        </button>
      </div>
    </aside>
  );
}
