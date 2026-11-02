import React from "react";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  subtext?: string;
  delta?: {
    value: string;
    isPositive: boolean;
    isGood?: boolean;
  };
  icon?: LucideIcon;
  variant?: "default" | "cyan" | "emerald" | "amber" | "rose";
  className?: string;
}

export function StatCard({
  title,
  value,
  subtext,
  delta,
  icon: Icon,
  variant = "default",
  className,
}: StatCardProps) {
  const iconBgs = {
    default: "bg-slate-800 text-slate-300",
    cyan: "bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 shadow-[0_0_12px_rgba(6,182,212,0.3)]",
    emerald: "bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 shadow-[0_0_12px_rgba(16,185,129,0.3)]",
    amber: "bg-amber-950/80 text-amber-400 border border-amber-800/60 shadow-[0_0_12px_rgba(245,158,11,0.3)]",
    rose: "bg-rose-950/80 text-rose-400 border border-rose-800/60 shadow-[0_0_12px_rgba(239,68,68,0.3)]",
  };

  return (
    <div
      className={cn(
        "command-panel rounded-xl p-4 flex flex-col justify-between hover:border-slate-600/50 transition-all",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <span className="text-xs font-medium text-slate-400 tracking-wider uppercase">
          {title}
        </span>
        {Icon && (
          <div className={cn("p-2 rounded-lg", iconBgs[variant])}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-3">
        <div className="text-2xl font-bold tracking-tight text-white font-mono">
          {value}
        </div>

        <div className="mt-1 flex items-center gap-2">
          {delta && (
            <span
              className={cn(
                "text-xs font-semibold px-1.5 py-0.5 rounded",
                delta.isGood ?? delta.isPositive
                  ? "bg-emerald-950/80 text-emerald-400 border border-emerald-800/50"
                  : "bg-rose-950/80 text-rose-400 border border-rose-800/50"
              )}
            >
              {delta.isPositive ? "+" : ""}
              {delta.value}
            </span>
          )}
          {subtext && <span className="text-xs text-slate-400">{subtext}</span>}
        </div>
      </div>
    </div>
  );
}

