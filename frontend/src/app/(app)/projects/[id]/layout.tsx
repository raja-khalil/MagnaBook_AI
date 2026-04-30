"use client";
import { usePathname } from "next/navigation";
import { WizardSteps, type Step } from "@/components/layout/WizardSteps";

const STEPS: Step[] = [
  { id: "upload", label: "Upload" },
  { id: "briefing", label: "Briefing" },
  { id: "prd", label: "PRD" },
  { id: "editor", label: "Editor" },
  { id: "export", label: "Exportar" },
];

function currentStep(pathname: string) {
  for (const s of [...STEPS].reverse()) {
    if (pathname.includes(`/${s.id}`)) return s.id;
  }
  return STEPS[0].id;
}

function completedBefore(stepId: string): string[] {
  const idx = STEPS.findIndex((s) => s.id === stepId);
  return STEPS.slice(0, idx).map((s) => s.id);
}

export default function ProjectLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const active = currentStep(pathname);
  const completed = completedBefore(active);

  return (
    <div className="flex flex-col gap-8">
      <div className="flex justify-center">
        <WizardSteps steps={STEPS} currentStep={active} completedSteps={completed} />
      </div>
      {children}
    </div>
  );
}
