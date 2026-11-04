"use client";

import React, { useState } from "react";
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
  LayoutGrid,
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

export type TabCategory = "ALL" | "MONITOR" | "SIMULATE" | "PRESCRIBE" | "GOVERN";

interface TabNavigationProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  criticalRiskCount?: number;
}

interface TabDef {
  id: ActiveTab;
  label: string;
  icon: React.ElementType;
  category: TabCategory;
  badge?: string | number;
}

export function TabNavigation({
  activeTab,
  onTabChange,
  criticalRiskCount = 0,
}: TabNavigationProps) {
  const [selectedCategory, setSelectedCategory] = useState<TabCategory>("ALL");

  const tabs: TabDef[] = [
    // 1. Monitor & Map
    { id: "situation_room", label: "Situation Room", icon: Compass, category: "MONITOR" },
    { id: "digital_twin", label: "Digital Twin", icon: Network, category: "MONITOR" },
    { id: "risks", label: "Risk Sentinels", icon: AlertTriangle, category: "MONITOR", badge: criticalRiskCount > 0 ? criticalRiskCount : undefined },
    { id: "ingestion", label: "Data Ingestion", icon: Database, category: "MONITOR" },
    { id: "connectors", label: "Cloud Connectors", icon: Cloud, category: "MONITOR" },

    // 2. Simulate & Forecast
    { id: "simulation", label: "Simulation Studio", icon: Sliders, category: "SIMULATE" },
    { id: "comparison", label: "Scenario Compare", icon: Split, category: "SIMULATE" },
    { id: "batch", label: "Batch & Sensitivity", icon: Layers, category: "SIMULATE" },
    { id: "forecasting", label: "Forecasting Studio", icon: TrendingUp, category: "SIMULATE" },

    // 3. Prescribe & Optimize
    { id: "optimization", label: "Prescriptive MILP", icon: Zap, category: "PRESCRIBE" },
    { id: "policy", label: "Policy Optimization", icon: Scale, category: "PRESCRIBE" },
    { id: "intelligence", label: "AI Copilot", icon: BrainCircuit, category: "PRESCRIBE" },
    { id: "rca", label: "Root Cause Trace", icon: GitMerge, category: "PRESCRIBE" },

    // 4. Financial & Govern
    { id: "waterfall", label: "Financial Waterfall", icon: BarChart3, category: "GOVERN" },
    { id: "reports", label: "Executive Reports", icon: FileText, category: "GOVERN" },
    { id: "governance", label: "Governance & Audit", icon: ShieldCheck, category: "GOVERN" },
  ];

  const categories: { id: TabCategory; label: string; count: number }[] = [
    { id: "ALL", label: "All Modules", count: 16 },
    { id: "MONITOR", label: "Monitor & Map", count: 5 },
    { id: "SIMULATE", label: "Simulate & Forecast", count: 4 },
    { id: "PRESCRIBE", label: "Prescribe & Optimize", count: 4 },
    { id: "GOVERN", label: "Financial & Govern", count: 3 },
  ];

  // Filter visible tabs based on category
  const visibleTabs = selectedCategory === "ALL"
    ? tabs
    : tabs.filter((t) => t.category === selectedCategory);

  return (
    <nav className="border-b border-white/[0.08] bg-command-900/80 backdrop-blur-md px-6 py-1.5 space-y-1">
      {/* Category Filter Pills (Compact Top Tier) */}
      <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1 text-[11px] font-mono">
        <span className="text-slate-500 uppercase tracking-widest text-[10px] mr-1 hidden sm:inline">
          Pillars:
        </span>
        {categories.map((cat) => {
          const isCatActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={cn(
                "px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider transition-colors shrink-0",
                isCatActive
                  ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                  : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
              )}
            >
              {cat.label} ({cat.count})
            </button>
          );
        })}
      </div>

      {/* Module Tabs Strip */}
      <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
        {visibleTabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={cn(
                "flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all whitespace-nowrap shrink-0",
                isActive
                  ? "bg-cyan-950/90 text-cyan-300 border border-cyan-800/80 shadow-[0_0_15px_rgba(6,182,212,0.25)]"
                  : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04] border border-transparent"
              )}
            >
              <Icon className={cn("w-3.5 h-3.5", isActive ? "text-cyan-400" : "text-slate-400")} />
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
