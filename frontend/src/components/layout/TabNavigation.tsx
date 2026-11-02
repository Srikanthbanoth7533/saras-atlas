"use client";

import React from "react";
import { cn } from "@/lib/utils";
import {
  Compass,
  Network,
  AlertTriangle,
  Sliders,
  Split,
  Zap,
  BarChart3,
  ShieldCheck,
  Layers,
  Scale,
  Database,
  BrainCircuit,
  GitMerge,
  TrendingUp,
  FileText,
  Cloud,
} from "lucide-react";

export type ActiveTab =
  | "situation_room"
  | "digital_twin"
  | "risks"
  | "simulation"
  | "comparison"
  | "optimization"
  | "batch"
  | "policy"
  | "ingestion"
  | "intelligence"
  | "rca"
  | "forecasting"
  | "reports"
  | "connectors"
  | "waterfall"
  | "governance";

interface TabNavigationProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  criticalRiskCount?: number;
}

export function TabNavigation({
  activeTab,
  onTabChange,
  criticalRiskCount = 0,
}: TabNavigationProps) {
  const tabs: { id: ActiveTab; label: string; icon: React.ElementType; badge?: string | number }[] = [
    { id: "situation_room", label: "Situation Room", icon: Compass },
    { id: "digital_twin", label: "Digital Twin", icon: Network },
    { id: "risks", label: "Risk Sentinels", icon: AlertTriangle, badge: criticalRiskCount > 0 ? criticalRiskCount : undefined },
    { id: "simulation", label: "Simulation Studio", icon: Sliders },
    { id: "comparison", label: "Scenario Compare", icon: Split },
    { id: "optimization", label: "Prescriptive MILP", icon: Zap },
    { id: "batch", label: "Batch & Sensitivity", icon: Layers },
    { id: "policy", label: "Policy Optimization", icon: Scale },
    { id: "ingestion", label: "Data Ingestion", icon: Database },
    { id: "intelligence", label: "AI Copilot", icon: BrainCircuit },
    { id: "rca", label: "Root Cause Trace", icon: GitMerge },
    { id: "forecasting", label: "Forecasting Studio", icon: TrendingUp },
    { id: "reports", label: "Executive Reports", icon: FileText },
    { id: "connectors", label: "Cloud Connectors", icon: Cloud },
    { id: "waterfall", label: "Financial Waterfall", icon: BarChart3 },
    { id: "governance", label: "Governance & Audit", icon: ShieldCheck },
  ];

  return (
    <nav className="border-b border-white/[0.08] bg-command-900/60 backdrop-blur-sm px-6">
      <div className="flex items-center gap-1 overflow-x-auto no-scrollbar py-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={cn(
                "flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all whitespace-nowrap",
                isActive
                  ? "bg-cyan-950/80 text-cyan-300 border border-cyan-800/60 shadow-[0_0_15px_rgba(6,182,212,0.25)]"
                  : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
              )}
            >
              <Icon className={cn("w-4 h-4", isActive ? "text-cyan-400" : "text-slate-400")} />
              <span>{tab.label}</span>
              {tab.badge !== undefined && (
                <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-rose-500 text-white animate-pulse">
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}

