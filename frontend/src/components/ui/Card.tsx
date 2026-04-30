import { type HTMLAttributes } from "react";
import { clsx } from "clsx";

type DivProps = HTMLAttributes<HTMLDivElement>;

export function Card({ className, ...props }: DivProps) {
  return <div className={clsx("rounded-xl border border-gray-200 bg-white shadow-sm", className)} {...props} />;
}

export function CardHeader({ className, ...props }: DivProps) {
  return <div className={clsx("border-b border-gray-100 px-6 py-4", className)} {...props} />;
}

export function CardBody({ className, ...props }: DivProps) {
  return <div className={clsx("px-6 py-5", className)} {...props} />;
}
