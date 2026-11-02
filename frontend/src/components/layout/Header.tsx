"use client";

import React from "react";
import { Badge } from "@/components/ui/Badge";
import { Activity, ShieldCheck, Database, Cpu, RefreshCw } from "lucide-react";
import { SystemHealth } from "@/lib/types";

interface HeaderProps {
  health: SystemHealth | null;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export function Header({ health, onRefresh, isRefreshing }: HeaderProps) {
  return (
    <header className="border-b border-white/[0.08] bg-command-950/90 backdrop-blur-md sticky top-0 z-50 px-6 py-3.5">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
        {/* Brand & Platform Identity */}
        <div className="flex items-center gap-3.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-[0_0_20px_rgba(6,182,212,0.4)]">
            <Activity className="h-5 w-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-lg font-black tracking-wider text-white uppercase font-mono">
                SARAS ATLAS
              </h1>
              <Badge variant="cyan" size="sm">
                PHASE 2 COCKPIT
              </Badge>
              <Badge variant="outline" size="sm" className="hidden sm:inline-flex text-slate-400">
                SYNTHETIC BENCHMARK
              </Badge>
            </div>
            <p className="text-xs text-slate-400">
              Commerce Resilience & Decision Simulation Platform • Vanguard Apparel Co. ($45M GMV)
            </p>
          </div>
        </div>

        {/* System Vitals & Health Indicators */}
        <div className="flex items-center flex-wrap gap-2.5">
          <div className="hidden lg:flex items-center gap-2 bg-command-900 border border-white/[0.06] rounded-lg px-3 py-1.5 text-xs text-slate-300 font-mono">
            <Database className="w-3.5 h-3.5 text-cyan-400" />
            <span>SQLite WAL</span>
            <span className="text-slate-600">•</span>
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            <span>OR-Tools SCIP</span>
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
