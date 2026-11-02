"use client";

import React, { useState, useEffect } from "react";
import {
  ShieldAlert,
  Award,
  Layers,
  Scale,
  DollarSign,
  TrendingUp,
  BarChart2,
  CheckCircle2,
  RefreshCw,
  GitBranch,
  Factory,
} from "lucide-react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
  Line,
  ComposedChart,
} from "recharts";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { formatCurrency, formatPercent } from "@/lib/utils";
import {
  PolicyOptimizationResponse,
  SupplierSourcingResponse,
} from "@/lib/types";
import {
  evaluateMitigationPolicies,
  optimizeSupplierSourcing,
} from "@/lib/api";

export default function DynamicPolicyOptimization() {
  const [evalResult, setEvalResult] = useState<PolicyOptimizationResponse | null>(null);
  const [sourcingResult, setSourcingResult] = useState<SupplierSourcingResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [stochasticDraws, setStochasticDraws] = useState<number>(25);

  useEffect(() => {
    loadEvaluations();
  }, []);

  const loadEvaluations = async () => {
    setIsLoading(true);
    try {
      const [pRes, sRes] = await Promise.all([
        evaluateMitigationPolicies(undefined, stochasticDraws),
        optimizeSupplierSourcing(),
      ]);
      setEvalResult(pRes);
      setSourcingResult(sRes);
    } catch (err) {
      console.error("Policy evaluation failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <Card>
        <CardHeader>
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 w-full">
            <div>
              <CardTitle>Dynamic Mitigation Policy Optimization</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Stochastic stress testing across uncertain supply delays, Pareto cost vs service-level frontiers, and risk-hedged dual sourcing
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex bg-slate-950 p-1 rounded-lg border border-white/[0.08] text-xs">
                <span className="text-slate-400 px-2 py-1 flex items-center">Draws:</span>
                {[15, 25, 50].map((d) => (
                  <button
                    key={d}
                    onClick={() => {
                      setStochasticDraws(d);
                      loadEvaluations();
                    }}
                    className={`px-2.5 py-1 rounded transition-colors ${
                      stochasticDraws === d ? "bg-cyan-500 text-slate-950 font-bold" : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
              <button
                onClick={loadEvaluations}
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
                Re-Evaluate
              </button>
            </div>
          </div>
        </CardHeader>

        {evalResult && (
          <div className="p-3.5 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-200 flex items-start gap-2.5 mt-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold uppercase tracking-wider text-emerald-300 mr-2">
                Executive Synthesis:
              </span>
              {evalResult.executive_verdict}
            </div>
          </div>
        )}
      </Card>

      {/* Policy Evaluation Matrix Table */}
      {evalResult && (
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Stochastic Policy Evaluation Matrix</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Evaluated across {evalResult.stochastic_draws} Monte Carlo shock realizations with Value-at-Risk (P10 VaR) and CVaR tail metrics
              </p>
            </div>
          </CardHeader>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Rank</th>
                  <th className="py-2.5 px-3">Policy Strategy</th>
                  <th className="py-2.5 px-3 text-right">Execution Outlay</th>
                  <th className="py-2.5 px-3 text-right">Expected Net CM</th>
                  <th className="py-2.5 px-3 text-right">Worst-Case (P10 VaR)</th>
                  <th className="py-2.5 px-3 text-right">CVaR (Tail Risk)</th>
                  <th className="py-2.5 px-3 text-right">Fill Rate</th>
                  <th className="py-2.5 px-3 text-center">Robustness</th>
                  <th className="py-2.5 px-3 text-center">Pareto Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {evalResult.evaluated_policies.map((p) => {
                  const isOptimal = p.rank === 1;

                  return (
                    <tr
                      key={p.policy_id}
                      className={`hover:bg-slate-800/40 transition-colors ${
                        isOptimal ? "bg-emerald-950/15" : ""
                      }`}
                    >
                      <td className="py-3 px-3 font-bold">
                        <span
                          className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] ${
                            isOptimal
                              ? "bg-amber-400 text-slate-950 font-black shadow-sm"
                              : "text-slate-400 bg-slate-800"
                          }`}
                        >
                          {p.rank}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-sans">
                        <div className="font-semibold text-slate-200 flex items-center gap-1.5">
                          {p.name}
                          {isOptimal && (
                            <Badge variant="emerald" size="sm">RECOMMENDED</Badge>
                          )}
                        </div>
                        <div className="text-[11px] text-slate-400 font-sans mt-0.5 line-clamp-1">
                          {p.description}
                        </div>
                      </td>
                      <td className="py-3 px-3 text-right text-slate-300">
                        {p.mitigation_cost > 0 ? formatCurrency(p.mitigation_cost) : "$0.00"}
                      </td>
                      <td className="py-3 px-3 text-right font-bold text-emerald-400">
                        {formatCurrency(p.mean_cm)}
                      </td>
                      <td className="py-3 px-3 text-right text-slate-300">
                        {formatCurrency(p.p10_cm)}
                      </td>
                      <td className="py-3 px-3 text-right text-rose-400">
                        {formatCurrency(p.cvar_90)}
                      </td>
                      <td className="py-3 px-3 text-right font-bold text-cyan-400">
                        {(p.mean_fill_rate * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-center">
                        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-200">
                          {p.robustness_score.toFixed(0)}/100
                        </span>
                      </td>
                      <td className="py-3 px-3 text-center">
                        {p.is_pareto_efficient ? (
                          <Badge variant="cyan" size="sm">PARETO OPTIMAL</Badge>
                        ) : (
                          <span className="text-slate-500 text-[11px]">Sub-Optimal</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Dual Charts: Pareto Frontier & Tail-Risk Distribution */}
      {evalResult && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <div>
                <CardTitle>Pareto Trade-Off Frontier: Cost vs Service Level</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Non-dominated mitigation strategies balancing capital budget vs order fill rate
                </p>
              </div>
            </CardHeader>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart
                  data={evalResult.pareto_frontier}
                  margin={{ top: 10, right: 30, left: 10, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="mitigation_cost"
                    stroke="#64748b"
                    tick={{ fill: "#94a3b8", fontSize: 11 }}
                    tickFormatter={(v) => `$${(v / 1000).toFixed(1)}k`}
                    label={{ value: "Mitigation Budget Outlay ($)", position: "insideBottom", offset: -10, fill: "#94a3b8", fontSize: 11 }}
                  />
                  <YAxis
                    dataKey="service_level"
                    stroke="#10b981"
                    tick={{ fill: "#10b981", fontSize: 11 }}
                    tickFormatter={(v) => `${v}%`}
                    domain={[70, 100]}
                    label={{ value: "Customer Fill Rate (%)", angle: -90, position: "insideLeft", fill: "#10b981", fontSize: 11 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#020617",
                      borderColor: "#334155",
                      borderRadius: "0.5rem",
                      fontSize: "12px",
                    }}
                    formatter={(val: any, name: string) => {
                      if (name === "Fill Rate") return [`${val}%`, name];
                      if (name === "Outlay") return [formatCurrency(val), name];
                      return [val, name];
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="service_level"
                    name="Efficient Frontier"
                    stroke="#06b6d4"
                    strokeWidth={2}
                    dot={{ r: 6, fill: "#06b6d4" }}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card>
            <CardHeader>
              <div>
                <CardTitle>Value-at-Risk & Tail Downside (CVaR)</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Comparing expected Net CM against 10th percentile worst-case downside
                </p>
              </div>
            </CardHeader>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={evalResult.evaluated_policies}
                  margin={{ top: 10, right: 20, left: 10, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="name"
                    stroke="#64748b"
                    tick={{ fill: "#94a3b8", fontSize: 10 }}
                    interval={0}
                    tickFormatter={(val) => val.split(" ")[0]}
                  />
                  <YAxis
                    stroke="#64748b"
                    tick={{ fill: "#94a3b8", fontSize: 11 }}
                    tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                    domain={[500000, "auto"]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#020617",
                      borderColor: "#334155",
                      borderRadius: "0.5rem",
                      fontSize: "12px",
                    }}
                    formatter={(val: any) => [formatCurrency(val), "Net CM"]}
                  />
                  <Legend />
                  <Bar dataKey="mean_cm" name="Expected Net CM" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="p10_cm" name="P10 Worst-Case VaR" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>
      )}

      {/* Sourcing Allocation Decision Card */}
      {sourcingResult && (
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Risk-Hedged Supplier Dual-Sourcing Optimizer</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Mathematical portfolio allocation balancing low-cost primary manufacturing vs agile secondary backup
              </p>
            </div>
          </CardHeader>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <StatCard
              title="Shenzhen Allocation"
              value={`${(sourcingResult.optimal_shenzhen_share * 100).toFixed(0)}%`}
              subtext="$45.15 unit COGS | 35-day lead"
              variant="cyan"
              icon={Factory}
            />
            <StatCard
              title="Saigon Allocation"
              value={`${(sourcingResult.optimal_saigon_share * 100).toFixed(0)}%`}
              subtext="$49.50 unit COGS | 18-day lead"
              variant="default"
              icon={GitBranch}
            />
            <StatCard
              title="Avoided Stockout Losses"
              value={formatCurrency(sourcingResult.net_portfolio_savings)}
              subtext="Net annual risk-hedged financial benefit"
              variant="emerald"
              icon={TrendingUp}
            />
            <StatCard
              title="Target Service Level"
              value={formatPercent(sourcingResult.optimal_service_level * 100)}
              subtext="Customer fulfillment reliability"
              variant="amber"
              icon={Scale}
            />
          </div>

          {/* Allocation Visual Bar */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs text-slate-300 font-semibold">
              <span>Shenzhen Primary Factory ({Math.round(sourcingResult.optimal_shenzhen_share * 100)}%)</span>
              <span>Saigon Backup Facility ({Math.round(sourcingResult.optimal_saigon_share * 100)}%)</span>
            </div>
            <div className="h-4 w-full bg-slate-900 rounded-full overflow-hidden flex border border-white/[0.08]">
              <div
                className="bg-indigo-600 h-full transition-all duration-500"
                style={{ width: `${sourcingResult.optimal_shenzhen_share * 100}%` }}
              />
              <div
                className="bg-cyan-500 h-full transition-all duration-500"
                style={{ width: `${sourcingResult.optimal_saigon_share * 100}%` }}
              />
            </div>
          </div>

          <div className="mt-4 p-3.5 rounded-lg bg-slate-950/70 border border-white/[0.08] text-xs text-slate-300">
            <span className="font-bold text-slate-100 uppercase tracking-wider mr-2">
              Optimization Rationale:
            </span>
            {sourcingResult.explainability}
          </div>
        </Card>
      )}
    </div>
  );
}
