import React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "cyan" | "emerald" | "amber" | "rose" | "purple" | "outline";
  size?: "sm" | "md";
}

export function Badge({
  className,
  variant = "default",
  size = "md",
  children,
  ...props
}: BadgeProps) {
  const variants = {
    default: "bg-slate-800 text-slate-300 border-slate-700",
    cyan: "bg-cyan-950/70 text-cyan-400 border-cyan-800/60 shadow-[0_0_10px_rgba(6,182,212,0.2)]",
    emerald: "bg-emerald-950/70 text-emerald-400 border-emerald-800/60 shadow-[0_0_10px_rgba(16,185,129,0.2)]",
    amber: "bg-amber-950/70 text-amber-400 border-amber-800/60 shadow-[0_0_10px_rgba(245,158,11,0.2)]",
    rose: "bg-rose-950/70 text-rose-400 border-rose-800/60 shadow-[0_0_10px_rgba(239,68,68,0.2)]",
    purple: "bg-purple-950/70 text-purple-400 border-purple-800/60 shadow-[0_0_10px_rgba(168,85,247,0.2)]",
    outline: "bg-transparent text-slate-300 border-slate-700/80",
  };

  const sizes = {
    sm: "px-2 py-0.5 text-xs font-medium",
    md: "px-2.5 py-1 text-xs font-semibold tracking-wide",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border transition-colors",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
