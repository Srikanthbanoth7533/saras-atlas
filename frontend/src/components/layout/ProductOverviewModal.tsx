"use client";

import React from "react";
import {
  Compass,
  Network,
  Sliders,
  AlertTriangle,
  BarChart3,
  Zap,
  ShieldCheck,
  Cpu,
  Database,
  ArrowRight,
  X,
  Play,
  CheckCircle2,
  Lock,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { ActiveTab } from "./TabNavigation";

interface ProductOverviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigateTab: (tab: ActiveTab) => void;
  onStartGuidedDemo: () => void;
}

export function ProductOverviewModal({
  isOpen,
  onClose,
  onNavigateTab,
  onStartGuidedDemo,
}: ProductOverviewModalProps) {
  if (!isOpen) return null;

  const pillars = [
    {
      icon: Network,
      color: "text-cyan-400 bg-cyan-950/80 border-cyan-800/60",
      title: "Digital Twin & Supply Chain Visibility",
      subtitle: "Multi-Echelon Network Modeling",
      description:
        "Full digital representation of facilities (3 DCs), 4 global suppliers, shipping lanes, and 50 SKUs. Tracks daily inventory conservation laws and echelon-level lead times.",
      tab: "digital_twin" as ActiveTab,
      highlight: "Conservation Laws Enforced",
    },
    {
      icon: Sliders,
      color: "text-indigo-400 bg-indigo-950/80 border-indigo-800/60",
      title: "Disruption Simulation Studio",
      subtitle: "Deterministic Daily Time-Step Shocks",
      description:
        "Simulates compound cascading shocks: Shenzhen port berthing delays (+21d), cross-zone freight surcharges (+28%), and viral social demand surges (+45%) with zero external cloud dependencies.",
      tab: "simulation" as ActiveTab,
      highlight: "Bit-for-Bit Deterministic",
    },
    {
      icon: AlertTriangle,
      color: "text-amber-400 bg-amber-950/80 border-amber-800/60",
      title: "Predictive Risk Sentinels",
      subtitle: "Autonomous Anomaly Detection",
      description:
        "Continuous algorithmic scanning for PO lead-time variance, safety-stock stockout runout horizons, and freight tariff anomalies before bottom-line damage manifests.",
      tab: "risks" as ActiveTab,
      highlight: "Early Warning Sentinels",
    },
    {
      icon: BarChart3,
      color: "text-emerald-400 bg-emerald-950/80 border-emerald-800/60",
      title: "Financial Impact & Waterfall",
      subtitle: "GAAP-Reconciled Margin Erosion",
      description:
        "Rigorously distinguishes $224,500.00 gross commercial revenue exposure from $129,844.32 net contribution margin erosion, providing a transparent, auditable bridge.",
      tab: "waterfall" as ActiveTab,
      highlight: "$224.5k Gross vs $129.8k Net",
    },
    {
      icon: Zap,
      color: "text-purple-400 bg-purple-950/80 border-purple-800/60",
      title: "Mathematical Optimization (MILP)",
      subtitle: "Google OR-Tools SCIP Prescriptive Engine",
      description:
        "Solves multi-echelon network trade-offs to proven global mathematical optimality. Exploits ground transfer efficiency ($25.35/$) up to the 800-unit ceiling, allocating $37,440 to 2,995 air units with $2.50 budget slack.",
      tab: "optimization" as ActiveTab,
      highlight: "SCIP Optimal • Duality Proof",
    },
    {
      icon: ShieldCheck,
      color: "text-rose-400 bg-rose-950/80 border-rose-800/60",
      title: "Governed Decisions & Two-Man Rule",
      subtitle: "Cryptographic Audit Ledger",
      description:
        "Dual-executive authorization enforced for allocations exceeding the $25,000 policy threshold. All approvals signed into a SHA-256 tamper-evident immutable ledger.",
      tab: "governance" as ActiveTab,
      highlight: "Dual Executive Sign-Off",
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-5xl bg-command-950 border border-cyan-500/30 rounded-2xl shadow-[0_0_50px_rgba(6,182,212,0.25)] overflow-hidden my-8">
        {/* Header Bar */}
        <div className="bg-gradient-to-r from-cyan-950/80 via-command-900 to-command-950 p-6 border-b border-white/[0.08] flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-bold tracking-widest text-cyan-400 uppercase bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800/60">
                PLATFORM CAPABILITIES OVERVIEW
              </span>
              <Badge variant="cyan" size="sm">
                ENTERPRISE V6.0
              </Badge>
              <Badge variant="outline" size="sm" className="text-slate-400">
                VANGUARD APPAREL BENCHMARK ($45M GMV)
              </Badge>
            </div>
            <h2 className="text-2xl font-black text-white tracking-wide font-mono uppercase mt-1">
              SARAS ATLAS — Commerce Resilience &amp; Decision Intelligence
            </h2>
            <p className="text-sm text-cyan-200/90 font-sans max-w-3xl">
              Model operational disruptions. Quantify financial exposure. Optimize mitigation decisions.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-lg bg-white/[0.04] hover:bg-white/[0.08] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto">
          {/* Executive Quick Actions */}
          <div className="bg-gradient-to-r from-cyan-950/60 via-indigo-950/40 to-command-900 p-4 rounded-xl border border-cyan-500/20 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                <Play className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-white">Guided Executive Demonstration</h4>
                <p className="text-xs text-slate-300">
                  Follow a curated 10-step walkthrough of the Shenzhen PO-9012 disruption cascade and SCIP optimization.
                </p>
              </div>
            </div>
            <button
              onClick={() => {
                onClose();
                onStartGuidedDemo();
              }}
              className="px-5 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider shadow-[0_0_20px_rgba(6,182,212,0.4)] flex items-center gap-2 shrink-0 transition-transform hover:scale-[1.02]"
            >
              <span>Launch 10-Step Tour</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          {/* 6 Value Pillars Grid */}
          <div>
            <h3 className="text-xs font-mono uppercase tracking-widest text-slate-400 mb-3 font-semibold">
              Six Enterprise Decision Pillars
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {pillars.map((pillar, idx) => {
                const Icon = pillar.icon;
                return (
                  <div
                    key={idx}
                    className="p-4 rounded-xl bg-command-900/80 border border-white/[0.06] hover:border-cyan-500/40 transition-all flex flex-col justify-between group"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <div className={`p-2 rounded-lg border ${pillar.color}`}>
                          <Icon className="w-4 h-4" />
                        </div>
                        <span className="text-[10px] font-mono font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
                          {pillar.highlight}
                        </span>
                      </div>
                      <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
                        {pillar.title}
                      </h4>
                      <div className="text-[11px] text-cyan-400/80 font-mono mb-2">
                        {pillar.subtitle}
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed font-sans">
                        {pillar.description}
                      </p>
                    </div>

                    <button
                      onClick={() => {
                        onClose();
                        onNavigateTab(pillar.tab);
                      }}
                      className="mt-4 pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs text-slate-300 hover:text-cyan-400 transition-colors"
                    >
                      <span className="font-mono text-[11px]">Open Module</span>
                      <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Technical Architecture Highlights */}
          <div className="p-4 rounded-xl bg-command-900 border border-white/[0.06] grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
            <div className="flex items-start gap-2.5">
              <Database className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase">Storage Engine</span>
                <span className="text-white font-bold">SQLite WAL + DuckDB</span>
                <span className="text-slate-400 text-[10px] block">Zero external database cost</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <Cpu className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase">Mathematical Solver</span>
                <span className="text-white font-bold">Google OR-Tools SCIP</span>
                <span className="text-slate-400 text-[10px] block">Global discrete optimality</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase">Memory Footprint</span>
                <span className="text-white font-bold">&lt; 350 MB RSS</span>
                <span className="text-slate-400 text-[10px] block">Runs on any local or free tier</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <Lock className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-slate-400 block text-[10px] uppercase">Audit Ledger</span>
                <span className="text-white font-bold">SHA-256 Cryptographic</span>
                <span className="text-slate-400 text-[10px] block">Tamper-evident verification</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-command-900/60 p-4 border-t border-white/[0.06] flex items-center justify-between text-xs text-slate-400 flex-wrap gap-2">
          <span>
            Synthetic Benchmark: Vanguard Apparel Co. ($45.0M Annual GMV, 150 SKUs, 3 DCs). No real customer data.
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-command-800 hover:bg-command-750 text-white font-semibold transition-colors"
          >
            Enter Platform
          </button>
        </div>
      </div>
    </div>
  );
}
