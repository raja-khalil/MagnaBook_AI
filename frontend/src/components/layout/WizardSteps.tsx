import { Check } from "lucide-react";
import { clsx } from "clsx";

export interface Step {
  id: string;
  label: string;
}

interface WizardStepsProps {
  steps: Step[];
  currentStep: string;
  completedSteps: string[];
}

export function WizardSteps({ steps, currentStep, completedSteps }: WizardStepsProps) {
  return (
    <nav aria-label="Progresso" className="flex items-center gap-0">
      {steps.map((step, i) => {
        const done = completedSteps.includes(step.id);
        const active = step.id === currentStep;
        return (
          <div key={step.id} className="flex items-center">
            <div className="flex flex-col items-center gap-1">
              <div
                className={clsx(
                  "flex h-8 w-8 items-center justify-center rounded-full border-2 text-xs font-bold transition-colors",
                  done && "border-brand-500 bg-brand-500 text-white",
                  active && !done && "border-brand-500 bg-white text-brand-600",
                  !done && !active && "border-gray-300 bg-white text-gray-400"
                )}
              >
                {done ? <Check size={14} /> : i + 1}
              </div>
              <span className={clsx("text-xs font-medium", active ? "text-brand-600" : "text-gray-400")}>
                {step.label}
              </span>
            </div>
            {i < steps.length - 1 && (
              <div className={clsx("mx-2 h-px w-10 flex-shrink-0", done ? "bg-brand-500" : "bg-gray-200")} />
            )}
          </div>
        );
      })}
    </nav>
  );
}
