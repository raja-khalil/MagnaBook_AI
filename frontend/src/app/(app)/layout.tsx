"use client";
import { Sidebar } from "@/components/layout/Sidebar";
import { useRequireAuth } from "@/hooks/useRequireAuth";
import { Spinner } from "@/components/ui/Spinner";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { isAuthed } = useRequireAuth();

  if (!isAuthed)
    return (
      <div className="flex h-screen items-center justify-center">
        <Spinner size="lg" className="text-brand-500" />
      </div>
    );

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">{children}</main>
    </div>
  );
}
