import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: "none" | "cyan" | "emerald" | "rose";
}

export function Card({
  className,
  glow = "none",
  children,
  ...props
}: CardProps) {
  const glowClasses = {
    none: "",
    cyan: "glow-cyan border-cyan-500/30",
    emerald: "glow-emerald border-emerald-500/30",
    rose: "glow-rose border-rose-500/30",
  };

  return (
    <div
      className={cn(
        "command-panel rounded-xl p-5 shadow-2xl transition-all duration-200",
        glowClasses[glow],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("flex items-center justify-between border-b border-white/[0.06] pb-3 mb-4", className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardTitle({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={cn("text-sm font-semibold tracking-wider uppercase text-slate-300 flex items-center gap-2", className)}
      {...props}
    >
      {children}
    </h3>
  );
}
