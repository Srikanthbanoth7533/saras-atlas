"use client";

import React from "react";
import { Badge } from "@/components/ui/Badge";
import {
  Activity,
  ShieldCheck,
  Database,
  Cpu,
  RefreshCw,
  Play,
  Info,
  Sparkles,
} from "lucide-react";
import { SystemHealth } from "@/lib/types";

interface HeaderProps {
  health: SystemHealth | null;
  onRefresh?: () => void;
  isRefreshing?: boolean;
  onOpenOverview?: () => void;
  onOpenDemo?: () => void;
}

export function Header({
  health,
  onRefresh,
  isRefreshing,
  onOpenOverview,
  onOpenDemo,
}: HeaderProps) {
  return (
    <header className="border-b border-white/[0.08] bg-command-950/95 backdrop-blur-md sticky top-0 z-50">
      {/* Prominent Demonstration & Attribution Banner */}
      <div className="bg-amber-950/50 border-b border-amber-500/30 px-6 py-1.5 text-[11px] text-amber-200/90 flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <span className="font-bold uppercase tracking-wider text-amber-400 bg-amber-900/60 px-1.5 py-0.5 rounded text-[10px] border border-amber-500/40">
            Portfolio Demo
          </span>
          <span>
            Independent engineering project using synthetic benchmarks (Vanguard Apparel Co. $45M GMV). Not affiliated with or endorsed by Saras Analytics.
          </span>
        </div>
        <div className="text-[10px] text-amber-400/80 font-mono hidden md:inline-flex">
          Strictly ₹0 Budget • Vercel Hobby + Render Free
        </div>
      </div>

      <div className="px-6 py-3 flex flex-col lg:flex-row lg:items-center justify-between gap-3">
        {/* Brand & Platform Identity */}
        <div className="flex items-start sm:items-center gap-3.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-[0_0_20px_rgba(6,182,212,0.4)] shrink-0 mt-0.5 sm:mt-0">
            <Activity className="h-5 w-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-base sm:text-lg font-black tracking-wider text-white uppercase font-mono">
                SARAS ATLAS
              </h1>
              <span className="text-slate-400 font-normal hidden sm:inline">—</span>
              <span className="text-xs sm:text-sm font-semibold text-cyan-300">
                Commerce Resilience &amp; Decision Intelligence
              </span>
              <Badge variant="cyan" size="sm">
                v6.0 ENTERPRISE
              </Badge>
              <Badge variant="outline" size="sm" className="hidden xl:inline-flex text-slate-400">
                SYNTHETIC BENCHMARK ($45M GMV)
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mt-0.5 font-sans">
              Model operational disruptions. Quantify financial exposure. Optimize mitigation decisions.
            </p>
          </div>
        </div>

        {/* Action Controls & System Vitals */}
        <div className="flex items-center flex-wrap gap-2.5">
          {/* Executive Overview & Guided Demo Buttons */}
          {onOpenOverview && (
            <button
              onClick={onOpenOverview}
              className="px-3 py-1.5 rounded-lg bg-command-900 hover:bg-command-800 border border-white/[0.08] text-slate-200 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Info className="w-3.5 h-3.5 text-cyan-400" />
              <span>Platform Overview</span>
            </button>
          )}

          {onOpenDemo && (
            <button
              onClick={onOpenDemo}
              className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-transform hover:scale-[1.02]"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>Executive Demo</span>
            </button>
          )}

          {/* System Vitals Badge */}
          <div className="hidden lg:flex items-center gap-2 bg-command-900 border border-white/[0.06] rounded-lg px-2.5 py-1.5 text-xs text-slate-300 font-mono">
            <Database className="w-3.5 h-3.5 text-cyan-400" />
            <span>SQLite WAL</span>
            <span className="text-slate-600">•</span>
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            <span>SCIP MILP</span>
            {health?.memory?.process_working_set_mb && (
              <>
                <span className="text-slate-600">•</span>
                <span className="text-emerald-400">
                  {health.memory.process_working_set_mb} MB RSS
                </span>
              </>
            )}
          </div>

          <Badge variant={health?.status === "HEALTHY" ? "emerald" : "amber"} size="md">
            <span className="w-1.5 h-1.5 rounded-full bg-current animate-ping" />
            {health?.status === "HEALTHY" ? "SYSTEM ONLINE" : "CONNECTING..."}
          </Badge>

          {onRefresh && (
            <button
              onClick={onRefresh}
              disabled={isRefreshing}
              className="p-2 rounded-lg bg-command-900 hover:bg-command-800 border border-white/[0.08] text-slate-300 hover:text-white transition-all disabled:opacity-50"
              title="Refresh Telemetry"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
