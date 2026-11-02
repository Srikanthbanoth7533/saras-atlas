"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { OptimizationRequest, OptimizationResult } from "@/lib/types";
import { Zap, CheckCircle2, DollarSign, Plane, Truck, Sliders, ShieldCheck, ArrowRight, Clock, Target } from "lucide-react";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";

interface OptimizationRecommendationsProps {
  onSolveOptimization: (req: OptimizationRequest) => Promise<OptimizationResult>;
  optimizationResult: OptimizationResult | null;
  onProceedToGovernance: (opt: OptimizationResult) => void;
  isLoading?: boolean;
}

export function OptimizationRecommendations({
  onSolveOptimization,
  optimizationResult,
  onProceedToGovernance,
  isLoading = false,
}: OptimizationRecommendationsProps) {
  const [budgetCeiling, setBudgetCeiling] = useState(40000);
  const [minFillRate, setMinFillRate] = useState(95);
  const [maxThrottle, setMaxThrottle] = useState(35);
  const [objective, setObjective] = useState<"MAXIMIZE_CONTRIBUTION_MARGIN" | "MINIMIZE_WORKING_CAPITAL" | "MAXIMIZE_FILL_RATE">("MAXIMIZE_CONTRIBUTION_MARGIN");

  const handleSolve = async () => {
    const req: OptimizationRequest = {
      capital_budget_ceiling: budgetCeiling,
      min_service_fill_rate: minFillRate / 100,
      max_ad_throttle_pct: maxThrottle / 100,
      target_sku: "APEX-JKT",
      objective: objective,
    };
    await onSolveOptimization(req);
  };

  const result = optimizationResult;

  return (
    <div className="space-y-6">
      {/* 1. MILP Solver Control & Configuration Panel */}
      <Card className="command-panel border-cyan-500/30">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 shadow-[0_0_12px_rgba(6,182,212,0.3)]">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <CardTitle>Google OR-Tools Prescriptive Optimization Engine</CardTitle>
              <p className="text-xs text-slate-400 mt-0.5">
                Solves mixed-integer multi-echelon network trade-offs to mathematical optimality using the SCIP solver
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="cyan" size="sm">SCIP SOLVER</Badge>
            <Badge variant="outline" size="sm">BIG-M MOQ ENFORCED</Badge>
          </div>
        </CardHeader>

        {/* Solver Constraints Form */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
            <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
              Working Capital Budget ($)
            </label>
            <input
              type="number"
              value={budgetCeiling}
              onChange={(e) => setBudgetCeiling(Number(e.target.value))}
              className="w-full bg-command-950 border border-white/[0.1] rounded px-3 py-1.5 font-mono text-sm text-white focus:outline-none focus:border-cyan-500"
            />
            <span className="text-[10px] text-slate-400 mt-1 block">Maximum allowed mitigation outlay</span>
          </div>

          <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
            <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
              Min Customer Fill Rate (%)
            </label>
            <input
              type="number"
              value={minFillRate}
              onChange={(e) => setMinFillRate(Number(e.target.value))}
              className="w-full bg-command-950 border border-white/[0.1] rounded px-3 py-1.5 font-mono text-sm text-white focus:outline-none focus:border-cyan-500"
            />
            <span className="text-[10px] text-slate-400 mt-1 block">Service level floor constraint</span>
          </div>

          <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
            <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
              Max Ad Throttle (%)
            </label>
            <input
              type="number"
              value={maxThrottle}
              onChange={(e) => setMaxThrottle(Number(e.target.value))}
              className="w-full bg-command-950 border border-white/[0.1] rounded px-3 py-1.5 font-mono text-sm text-white focus:outline-none focus:border-cyan-500"
            />
            <span className="text-[10px] text-slate-400 mt-1 block">Upper bound on marketing dampening</span>
          </div>

          <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3 flex flex-col justify-between">
            <div>
              <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
                Optimization Objective
              </label>
              <select
                value={objective}
                onChange={(e) => setObjective(e.target.value as any)}
                className="w-full bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-cyan-300 focus:outline-none focus:border-cyan-500"
              >
                <option value="MAXIMIZE_CONTRIBUTION_MARGIN">Maximize Net Contribution Margin</option>
                <option value="MINIMIZE_WORKING_CAPITAL">Minimize Cash Outlay</option>
                <option value="MAXIMIZE_FILL_RATE">Maximize Customer Fill Rate</option>
              </select>
            </div>
            <button
              onClick={handleSolve}
              disabled={isLoading}
              className="mt-2 w-full py-2 rounded bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider flex items-center justify-center gap-1.5 transition-all shadow-[0_0_15px_rgba(6,182,212,0.4)] disabled:opacity-50"
            >
              <Zap className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
              <span>{isLoading ? "Solving..." : "Run Optimization"}</span>
            </button>
          </div>
        </div>
      </Card>

      {/* 2. Solver Result & Prescriptive Decision Action Cards */}
      {result && (
        <div className="space-y-6">
          {/* Telemetry Header */}
          <div className="command-panel rounded-xl p-4 border border-emerald-500/40 bg-gradient-to-r from-emerald-950/40 via-command-900/80 to-command-950 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">
                    OR-TOOLS SCIP SOLVER CONVERGED
                  </span>
                  <Badge variant="emerald" size="sm">{result.status}</Badge>
                </div>
                <p className="text-xs text-slate-300 mt-0.5">
                  Global mathematical optimum found in <span className="font-mono font-bold text-white">{result.solve_time_ms} ms</span>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right font-mono">
                <span className="text-[10px] text-slate-400 uppercase block">Total Capital Outlay</span>
                <span className="text-sm font-bold text-cyan-400">{formatCurrency(result.capital_required)}</span>
              </div>
              <button
                onClick={() => onProceedToGovernance(result)}
                className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 shadow-[0_0_15px_rgba(16,185,129,0.3)] transition-all"
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Submit to Two-Man Sign-Off</span>
              </button>
            </div>
          </div>

          {/* 3 Prescriptive Action Decision Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Action 1: Air Freight */}
            <Card className="command-panel border-cyan-500/30">
              <div className="flex items-start justify-between">
                <div className="p-2.5 rounded-lg bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                  <Plane className="w-5 h-5" />
                </div>
                <Badge variant="cyan" size="sm">ACTION 1 • SUPPLY</Badge>
              </div>
              <h4 className="text-sm font-bold text-white mt-3">Expedited Backup Factory Air Freight</h4>
              <p className="text-xs text-slate-400 mt-1">
                Air-freight high-velocity sizes (M, L) directly from backup factory in Saigon, Vietnam to Reno 3PL.
              </p>
              <div className="mt-4 pt-3 border-t border-white/[0.06] flex items-baseline justify-between font-mono">
                <span className="text-xs text-slate-400">Order Quantity:</span>
                <span className="text-base font-bold text-cyan-400">{formatNumber(result.recommended_air_freight_units)} units</span>
              </div>
              <div className="mt-1 flex items-baseline justify-between font-mono text-xs">
                <span className="text-slate-400">Unit Cost & Total:</span>
                <span className="text-slate-300">$12.50/unit • {formatCurrency(result.recommended_air_freight_units * 12.50)}</span>
              </div>
            </Card>

            {/* Action 2: Ground Transfer */}
            <Card className="command-panel border-emerald-500/30">
              <div className="flex items-start justify-between">
                <div className="p-2.5 rounded-lg bg-emerald-950/80 text-emerald-400 border border-emerald-800/60">
                  <Truck className="w-5 h-5" />
                </div>
                <Badge variant="emerald" size="sm">ACTION 2 • INVENTORY</Badge>
              </div>
              <h4 className="text-sm font-bold text-white mt-3">Inter-Warehouse Stock Transfer</h4>
              <p className="text-xs text-slate-400 mt-1">
                LTL ground transfer of surplus stock from Allentown (East Coast) to Reno (West Coast).
              </p>
              <div className="mt-4 pt-3 border-t border-white/[0.06] flex items-baseline justify-between font-mono">
                <span className="text-xs text-slate-400">Transfer Units:</span>
                <span className="text-base font-bold text-emerald-400">{formatNumber(result.recommended_transfer_units)} units</span>
              </div>
              <div className="mt-1 flex items-baseline justify-between font-mono text-xs">
                <span className="text-slate-400">Unit Cost & Total:</span>
                <span className="text-slate-300">$3.20/unit • {formatCurrency(result.recommended_transfer_units * 3.20)}</span>
              </div>
            </Card>

            {/* Action 3: Marketing Throttle */}
            <Card className="command-panel border-indigo-500/30">
              <div className="flex items-start justify-between">
                <div className="p-2.5 rounded-lg bg-indigo-950/80 text-indigo-400 border border-indigo-800/60">
                  <Sliders className="w-5 h-5" />
                </div>
                <Badge variant="purple" size="sm">ACTION 3 • DEMAND</Badge>
              </div>
              <h4 className="text-sm font-bold text-white mt-3">Tactical Paid Ad Spend Throttle</h4>
              <p className="text-xs text-slate-400 mt-1">
                Throttle Meta/Google campaigns on Apex Jacket to prevent burning ad spend on out-of-stock sizes.
              </p>
              <div className="mt-4 pt-3 border-t border-white/[0.06] flex items-baseline justify-between font-mono">
                <span className="text-xs text-slate-400">Ad Throttle:</span>
                <span className="text-base font-bold text-purple-400">{formatPercent(result.recommended_ad_throttle_pct)} reduction</span>
              </div>
              <div className="mt-1 flex items-baseline justify-between font-mono text-xs">
                <span className="text-slate-400">Protected CM Lift:</span>
                <span className="text-emerald-400">Preserves margin rate at {formatPercent(result.projected_contribution_margin_pct)}</span>
              </div>
            </Card>
          </div>

          {/* Rationale Synthesis */}
          <Card className="command-panel border-white/[0.08]">
            <CardHeader>
              <CardTitle>
                <Target className="w-4 h-4 text-cyan-400" />
                <span>Mathematical Optimization Rationale</span>
              </CardTitle>
              <Badge variant="cyan" size="sm">EXPLAINABLE PRESCRIPTION</Badge>
            </CardHeader>
            <p className="text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-line p-3 bg-command-950/80 rounded-lg border border-white/[0.04]">
              {result.rationale}
            </p>
          </Card>
        </div>
      )}
    </div>
  );
}

