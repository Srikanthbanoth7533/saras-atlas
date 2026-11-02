"use client";

import React from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import {
  AlertOctagon,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  DollarSign,
  Package,
  Clock,
  ArrowRight,
  Zap,
} from "lucide-react";
import { SimulationResponse, ActiveRisk } from "@/lib/types";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";

interface SituationRoomProps {
  unmitigatedSim: SimulationResponse | null;
  mitigatedSim: SimulationResponse | null;
  activeRisks: ActiveRisk[];
  onTriggerOptimization: () => void;
  onOpenSimulation: () => void;
  onOpenGovernance: () => void;
}

export function SituationRoom({
  unmitigatedSim,
  mitigatedSim,
  activeRisks,
  onTriggerOptimization,
  onOpenSimulation,
  onOpenGovernance,
}: SituationRoomProps) {
  const isMitigated = !!mitigatedSim;
  const currentSim = isMitigated ? mitigatedSim : unmitigatedSim;

  const revenue = currentSim?.summary_scorecard.net_revenue ?? 1425600;
  const contributionMargin = currentSim?.summary_scorecard.net_contribution_margin ?? 461800;
  const cmPct = currentSim?.summary_scorecard.contribution_margin_pct ?? 0.3239;
  const stockoutDays = currentSim?.summary_scorecard.stockout_days ?? 0;
  const lostOrders = currentSim?.summary_scorecard.unfulfilled_lost_orders ?? 0;
  const capitalRequired = currentSim?.summary_scorecard.working_capital_required ?? 0;

  return (
    <div className="space-y-6">
      {/* 1. Critical Disruption Situation Alert Banner */}
      <div className="relative overflow-hidden rounded-xl border border-rose-500/30 bg-gradient-to-r from-rose-950/70 via-command-900/90 to-command-950 p-5 shadow-2xl">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-xl bg-rose-900/60 border border-rose-700/60 shadow-[0_0_15px_rgba(239,68,68,0.4)]">
              <AlertOctagon className="h-7 w-7 text-rose-400 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2.5 flex-wrap">
                <span className="text-xs font-mono font-bold tracking-widest text-rose-400 uppercase">
                  ACTIVE FLAGSHIP DISRUPTION CASCADE
                </span>
                <Badge variant="rose" size="sm">
                  HIGH SEVERITY
                </Badge>
                <Badge variant="outline" size="sm">
                  VESSEL: EVER FORWARD
                </Badge>
              </div>
              <h2 className="text-lg md:text-xl font-bold text-white mt-1">
                Compound Shock: Trans-Pacific Berthing Delay (+21d) • Freight Surcharge (+28%) • Viral Demand (+45%)
              </h2>
              <p className="text-xs text-slate-300 mt-1 max-w-4xl">
                Inbound shipment <strong className="text-white">PO-9012</strong> (10,000 units of Hero SKU Apex Jacket) is delayed at Long Beach Port. 
                Reno 3PL runs out of stock on Day 9. Without mitigation, cross-zone fallback drains Allentown, causing a{" "}
                <span className="text-rose-400 font-bold">10-day national stockout</span> and destroying{" "}
                <span className="text-rose-400 font-bold">$290k+ in net contribution margin</span>.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5 self-start lg:self-center">
            <button
              onClick={onTriggerOptimization}
              className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider shadow-[0_0_20px_rgba(6,182,212,0.4)] flex items-center gap-2 transition-all transform hover:scale-[1.02]"
            >
              <Zap className="w-4 h-4" />
              <span>Solve with OR-Tools MILP</span>
            </button>
            <button
              onClick={onOpenSimulation}
              className="px-4 py-2.5 rounded-lg bg-command-800 hover:bg-command-750 border border-white/[0.1] text-slate-200 text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5 transition-all"
            >
              <span>Adjust Levers</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* 2. Executive Situation Assessment & Resilience State */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="command-panel rounded-xl p-4 border border-white/[0.08]">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
            Operational State
          </span>
          <div className="flex items-center gap-2.5 mt-2">
            {stockoutDays === 0 ? (
              <>
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <span className="text-base font-bold text-emerald-400">RESILIENT (PROTECTED)</span>
              </>
            ) : (
              <>
                <ShieldAlert className="w-5 h-5 text-rose-400 animate-pulse" />
                <span className="text-base font-bold text-rose-400">CRITICAL STOCKOUT</span>
              </>
            )}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            {stockoutDays === 0
              ? "Optimal air-freight & transfer bridging 100% of demand"
              : `${stockoutDays} dark days projected without mitigation`}
          </p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-white/[0.08]">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
            Commercial Exposure
          </span>
          <div className="text-xl font-bold font-mono text-white mt-1">
            {formatCurrency(lostOrders * 180.00)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            {lostOrders > 0
              ? `${formatNumber(lostOrders)} unfulfilled customer orders`
              : "Zero lost sales • 100% customer demand captured"}
          </p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-white/[0.08]">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
            Required Mitigation Capital
          </span>
          <div className="text-xl font-bold font-mono text-cyan-400 mt-1">
            {formatCurrency(capitalRequired)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Self-funding working capital • Within $40k budget ceiling
          </p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-white/[0.08] flex flex-col justify-between">
          <div>
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              Governance Gate
            </span>
            <div className="text-sm font-bold text-amber-400 mt-1 flex items-center gap-1.5">
              <span>Two-Man Sign-Off Required</span>
            </div>
          </div>
          <button
            onClick={onOpenGovernance}
            className="mt-2 text-xs text-indigo-400 hover:text-indigo-300 font-semibold underline flex items-center gap-1"
          >
            Review Dual Authorization Gate <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* 3. Enterprise KPI Matrix */}
      <div>
        <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
          <span>Enterprise Real-Time Financial & Operational Indicators (90-Day Projected)</span>
          <span className="h-px flex-1 bg-white/[0.08]" />
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
          <StatCard
            title="Net Gross Revenue"
            value={formatCurrency(revenue)}
            subtext="90-day trajectory"
            variant="cyan"
            delta={
              unmitigatedSim && mitigatedSim
                ? {
                    value: formatCurrency(mitigatedSim.summary_scorecard.net_revenue - unmitigatedSim.summary_scorecard.net_revenue),
                    isPositive: true,
                    isGood: true,
                  }
                : undefined
            }
            icon={DollarSign}
          />

          <StatCard
            title="Contribution Margin ($)"
            value={formatCurrency(contributionMargin)}
            subtext={`Margin rate: ${formatPercent(cmPct)}`}
            variant="emerald"
            delta={
              unmitigatedSim && mitigatedSim
                ? {
                    value: formatCurrency(mitigatedSim.summary_scorecard.net_contribution_margin - unmitigatedSim.summary_scorecard.net_contribution_margin),
                    isPositive: true,
                    isGood: true,
                  }
                : undefined
            }
            icon={TrendingUp}
          />

          <StatCard
            title="CM Rate (%)"
            value={formatPercent(cmPct)}
            subtext="GAAP waterfall"
            variant="emerald"
            delta={
              unmitigatedSim && mitigatedSim
                ? {
                    value: formatPercent(mitigatedSim.summary_scorecard.contribution_margin_pct - unmitigatedSim.summary_scorecard.contribution_margin_pct),
                    isPositive: true,
                    isGood: true,
                  }
                : undefined
            }
            icon={TrendingUp}
          />

          <StatCard
            title="Stockout Duration"
            value={`${stockoutDays} Days`}
            subtext={stockoutDays === 0 ? "Continuous fulfillment" : "Dark window duration"}
            variant={stockoutDays === 0 ? "emerald" : "rose"}
            icon={Clock}
          />

          <StatCard
            title="Orders Fulfilled"
            value={formatNumber(currentSim?.summary_scorecard.total_orders_fulfilled ?? 7920)}
            subtext={`${formatNumber(lostOrders)} lost orders`}
            variant="cyan"
            icon={Package}
          />

          <StatCard
            title="Active Sentinel Risks"
            value={`${activeRisks.length} Risks`}
            subtext={`${activeRisks.filter((r) => r.severity === "CRITICAL").length} Critical`}
            variant={activeRisks.some((r) => r.severity === "CRITICAL") ? "rose" : "amber"}
            icon={AlertOctagon}
          />
        </div>
      </div>

      {/* 4. Executive Narrative Brief */}
      {currentSim?.executive_narrative && (
        <Card className="border-cyan-500/20 bg-command-900/90">
          <CardHeader>
            <CardTitle>
              <Zap className="w-4 h-4 text-cyan-400" />
              <span>Executive Situational Narrative & Variance Decomposition</span>
            </CardTitle>
            <Badge variant="cyan" size="sm">
              SYNTHESIZED INSIGHT
            </Badge>
          </CardHeader>
          <div className="font-mono text-xs text-slate-300 leading-relaxed whitespace-pre-line p-3 bg-command-950/80 rounded-lg border border-white/[0.04]">
            {currentSim.executive_narrative}
          </div>
        </Card>
      )}
    </div>
  );
}

