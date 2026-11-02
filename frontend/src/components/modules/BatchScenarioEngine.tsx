"use client";

import React, { useState, useEffect } from "react";
import {
  Layers,
  Play,
  TrendingUp,
  TrendingDown,
  Activity,
  Sliders,
  CheckCircle,
  AlertTriangle,
  Cpu,
  Clock,
  RefreshCw,
  Award,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  AreaChart,
  Area,
} from "recharts";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { formatCurrency, formatPercent } from "@/lib/utils";
import {
  BatchScenarioItem,
  BatchRunResponse,
  SensitivitySweepResponse,
} from "@/lib/types";
import {
  fetchBenchmarkScenarios,
  runBatchSimulation,
  runSensitivitySweep,
} from "@/lib/api";

export default function BatchScenarioEngine() {
  const [scenarioCount, setScenarioCount] = useState<number>(10);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [batchResult, setBatchResult] = useState<BatchRunResponse | null>(null);
  const [activeSubTab, setActiveSubTab] = useState<"ranking" | "sensitivity">("ranking");

  // Sensitivity State
  const [sweepParam, setSweepParam] = useState<"supplier_delay" | "freight_surcharge" | "demand_surge">("supplier_delay");
  const [sweepSteps, setSweepSteps] = useState<number>(10);
  const [isSweeping, setIsSweeping] = useState<boolean>(false);
  const [sensitivityResult, setSensitivityResult] = useState<SensitivitySweepResponse | null>(null);

  useEffect(() => {
    executeBatch(10);
    executeSensitivity("supplier_delay", 10);
  }, []);

  const executeBatch = async (count: number) => {
    setIsRunning(true);
    setScenarioCount(count);
    try {
      const benchmarkItems = await fetchBenchmarkScenarios(count);
      const res = await runBatchSimulation(benchmarkItems, `Resilience Benchmark ${count} Scenarios`, true);
      setBatchResult(res);
    } catch (err) {
      console.error("Batch run failed:", err);
    } finally {
      setIsRunning(false);
    }
  };

  const executeSensitivity = async (
    param: "supplier_delay" | "freight_surcharge" | "demand_surge",
    steps: number
  ) => {
    setIsSweeping(true);
    setSweepParam(param);
    try {
      const minVal = param === "supplier_delay" ? 0 : param === "freight_surcharge" ? 0.05 : 1.0;
      const maxVal = param === "supplier_delay" ? 60 : param === "freight_surcharge" ? 0.60 : 2.2;
      const res = await runSensitivitySweep(param, minVal, maxVal, steps);
      setSensitivityResult(res);
    } catch (err) {
      console.error("Sensitivity sweep failed:", err);
    } finally {
      setIsSweeping(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Controls Bar */}
      <Card>
        <CardHeader>
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 w-full">
            <div>
              <CardTitle>Multi-Scenario Batch Simulation & Sensitivity Engine</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                High-throughput parallel scenario exploration, stochastic ranking, and parametric sensitivity sweeps
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400 flex items-center gap-1.5 mr-2">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                4 Worker Threads
              </span>
              <div className="flex bg-slate-950 p-1 rounded-lg border border-white/[0.08]">
                {[10, 50, 100].map((count) => (
                  <button
                    key={count}
                    onClick={() => executeBatch(count)}
                    disabled={isRunning}
                    className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                      scenarioCount === count
                        ? "bg-cyan-500 text-slate-950 font-bold shadow-sm"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {count} Scenarios
                  </button>
                ))}
              </div>
              <button
                onClick={() => executeBatch(scenarioCount)}
                disabled={isRunning}
                className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors disabled:opacity-50"
              >
                <Play className={`w-3.5 h-3.5 ${isRunning ? "animate-spin" : ""}`} />
                {isRunning ? "Running..." : "Re-Run Batch"}
              </button>
            </div>
          </div>
        </CardHeader>

        {/* KPI Scorecards */}
        {batchResult && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-2">
            <StatCard
              title="Throughput & Latency"
              value={`${batchResult.scenarios_per_second.toFixed(1)}/s`}
              subtext={`${batchResult.completed_scenarios} scenarios in ${batchResult.total_execution_ms.toFixed(0)} ms`}
              variant="cyan"
              icon={Activity}
            />
            <StatCard
              title="Best Case Scenario"
              value={formatCurrency(batchResult.best_case.scorecard.net_contribution_margin)}
              subtext={`Score ${batchResult.best_case.composite_score.toFixed(0)} • ${batchResult.best_case.scenario_name.substring(0, 22)}`}
              variant="emerald"
              icon={TrendingUp}
            />
            <StatCard
              title="Worst Case Downside"
              value={formatCurrency(batchResult.worst_case.scorecard.net_contribution_margin)}
              subtext={`${batchResult.worst_case.scorecard.stockout_days} stockout days • Score ${batchResult.worst_case.composite_score.toFixed(0)}`}
              variant="rose"
              icon={TrendingDown}
            />
            <StatCard
              title="Mean Customer Fill Rate"
              value={formatPercent(batchResult.summary_stats.mean_fill_rate * 100)}
              subtext={`Min ${(batchResult.summary_stats.min_fill_rate * 100).toFixed(1)}% | Max ${(batchResult.summary_stats.max_fill_rate * 100).toFixed(1)}%`}
              variant="amber"
              icon={Award}
            />
          </div>
        )}
      </Card>

      {/* Sub-Tab Navigation */}
      <div className="flex gap-2 border-b border-white/[0.08] pb-2">
        <button
          onClick={() => setActiveSubTab("ranking")}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === "ranking"
              ? "bg-slate-800 text-cyan-400 border border-slate-700 shadow-sm"
              : "text-slate-400 hover:text-slate-200"
          }`}
        >
          <Layers className="w-4 h-4" />
          Scenario Ranking Leaderboard ({batchResult?.completed_scenarios ?? 0})
        </button>
        <button
          onClick={() => setActiveSubTab("sensitivity")}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === "sensitivity"
              ? "bg-slate-800 text-cyan-400 border border-slate-700 shadow-sm"
              : "text-slate-400 hover:text-slate-200"
          }`}
        >
          <Sliders className="w-4 h-4" />
          Parametric Sensitivity Analysis Studio
        </button>
      </div>

      {/* View 1: Scenario Ranking Leaderboard */}
      {activeSubTab === "ranking" && batchResult && (
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Multi-Criteria Scenario Ranking Leaderboard</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Ranked deterministically across Contribution Margin (50%), Order Fill Rate (30%), and Stockout Days Avoidance (20%)
              </p>
            </div>
          </CardHeader>
          <div className="overflow-x-auto max-h-[520px]">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-slate-950/80 sticky top-0 border-b border-slate-800 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Rank</th>
                  <th className="py-2.5 px-3">Scenario ID & Title</th>
                  <th className="py-2.5 px-3">Shocks (Delay / Surcharge / Surge)</th>
                  <th className="py-2.5 px-3">Mitigations</th>
                  <th className="py-2.5 px-3 text-right">Net Revenue</th>
                  <th className="py-2.5 px-3 text-right">Net CM</th>
                  <th className="py-2.5 px-3 text-right">Fill Rate</th>
                  <th className="py-2.5 px-3 text-center">Stockouts</th>
                  <th className="py-2.5 px-3 text-right">Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {batchResult.ranked_results.map((res) => {
                  const fr =
                    res.scorecard.total_orders_fulfilled /
                    Math.max(1, res.scorecard.total_orders_fulfilled + res.scorecard.unfulfilled_lost_orders);
                  const isTop3 = res.rank <= 3;
                  const isWorst = res.rank === batchResult.ranked_results.length;

                  return (
                    <tr
                      key={res.scenario_id}
                      className={`hover:bg-slate-800/40 transition-colors ${
                        isTop3
                          ? "bg-emerald-950/15"
                          : isWorst
                          ? "bg-rose-950/20"
                          : ""
                      }`}
                    >
                      <td className="py-2.5 px-3 font-bold">
                        <span
                          className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] ${
                            res.rank === 1
                              ? "bg-amber-400 text-slate-950 font-black shadow-sm"
                              : res.rank === 2
                              ? "bg-slate-300 text-slate-950 font-bold"
                              : res.rank === 3
                              ? "bg-amber-700 text-white font-bold"
                              : "text-slate-400"
                          }`}
                        >
                          {res.rank}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 font-sans">
                        <div className="font-semibold text-slate-200">{res.scenario_name}</div>
                        <div className="text-[11px] text-slate-400 font-mono">{res.scenario_id}</div>
                      </td>
                      <td className="py-2.5 px-3 text-slate-300 font-sans text-[11px]">
                        {res.shocks_summary.delays?.[0]?.delay_days ?? 0}d delay | +
                        {Math.round((res.shocks_summary.freight_surcharges?.[0]?.surcharge_percentage ?? 0) * 100)}% fuel |{" "}
                        {Math.round(((res.shocks_summary.demand_surges?.[0]?.demand_multiplier ?? 1.0) - 1.0) * 100)}% surge
                      </td>
                      <td className="py-2.5 px-3 text-slate-400 font-sans text-[11px]">
                        {res.mitigations_summary.emergency_air_freight_units > 0 && (
                          <span className="text-cyan-400 mr-2">Air: {res.mitigations_summary.emergency_air_freight_units}</span>
                        )}
                        {res.mitigations_summary.inter_warehouse_transfer_units > 0 && (
                          <span className="text-emerald-400 mr-2">Xfer: {res.mitigations_summary.inter_warehouse_transfer_units}</span>
                        )}
                        {res.mitigations_summary.ad_spend_throttle_percentage > 0 && (
                          <span className="text-amber-400">Ad: {Math.round(res.mitigations_summary.ad_spend_throttle_percentage * 100)}%</span>
                        )}
                        {res.mitigations_summary.emergency_air_freight_units === 0 &&
                          res.mitigations_summary.inter_warehouse_transfer_units === 0 &&
                          res.mitigations_summary.ad_spend_throttle_percentage === 0 && (
                            <span className="text-slate-500 italic">None (Unmitigated)</span>
                          )}
                      </td>
                      <td className="py-2.5 px-3 text-right text-slate-300">
                        {formatCurrency(res.scorecard.net_revenue)}
                      </td>
                      <td
                        className={`py-2.5 px-3 text-right font-bold ${
                          res.scorecard.net_contribution_margin >= 760000
                            ? "text-emerald-400"
                            : res.scorecard.net_contribution_margin < 600000
                            ? "text-rose-400"
                            : "text-slate-200"
                        }`}
                      >
                        {formatCurrency(res.scorecard.net_contribution_margin)}
                      </td>
                      <td className="py-2.5 px-3 text-right text-slate-300">
                        {(fr * 100).toFixed(1)}%
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        {res.scorecard.stockout_days > 0 ? (
                          <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-950/60 text-rose-400 border border-rose-800/40">
                            {res.scorecard.stockout_days}d
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">
                            0d
                          </span>
                        )}
                      </td>
                      <td className="py-2.5 px-3 text-right font-bold text-cyan-400">
                        {res.composite_score.toFixed(1)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* View 2: Parametric Sensitivity Analysis Studio */}
      {activeSubTab === "sensitivity" && (
        <Card>
          <CardHeader>
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 w-full">
              <div>
                <CardTitle>Parametric Sensitivity Sweep Controller</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Evaluate marginal elasticity and resilience decay curves by sweeping individual shock parameters
                </p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex bg-slate-950 p-1 rounded-lg border border-white/[0.08]">
                  <button
                    onClick={() => executeSensitivity("supplier_delay", sweepSteps)}
                    className={`px-3 py-1 text-xs rounded-md font-semibold transition-all ${
                      sweepParam === "supplier_delay"
                        ? "bg-cyan-500 text-slate-950"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    Supplier Delay (0–60d)
                  </button>
                  <button
                    onClick={() => executeSensitivity("freight_surcharge", sweepSteps)}
                    className={`px-3 py-1 text-xs rounded-md font-semibold transition-all ${
                      sweepParam === "freight_surcharge"
                        ? "bg-cyan-500 text-slate-950"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    Freight Surcharge (5–60%)
                  </button>
                  <button
                    onClick={() => executeSensitivity("demand_surge", sweepSteps)}
                    className={`px-3 py-1 text-xs rounded-md font-semibold transition-all ${
                      sweepParam === "demand_surge"
                        ? "bg-cyan-500 text-slate-950"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    Demand Surge (0–120%)
                  </button>
                </div>

                <button
                  onClick={() => executeSensitivity(sweepParam, sweepSteps)}
                  disabled={isSweeping}
                  className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSweeping ? "animate-spin" : ""}`} />
                  {isSweeping ? "Sweeping..." : "Run Sweep"}
                </button>
              </div>
            </div>
          </CardHeader>

          {sensitivityResult && (
            <div className="space-y-6 mt-2">
              <div className="p-3.5 rounded-lg bg-cyan-950/20 border border-cyan-800/40 text-xs text-cyan-200 flex items-start gap-2.5">
                <Activity className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold uppercase tracking-wider text-cyan-300 mr-2">
                    Elasticity Gradient ({sensitivityResult.elasticity_score.toFixed(3)}):
                  </span>
                  {sensitivityResult.executive_insight}
                </div>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart
                    data={sensitivityResult.points}
                    margin={{ top: 10, right: 30, left: 20, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="cmGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis
                      dataKey="param_label"
                      stroke="#64748b"
                      tick={{ fill: "#94a3b8", fontSize: 11 }}
                    />
                    <YAxis
                      yAxisId="cm"
                      stroke="#06b6d4"
                      tick={{ fill: "#06b6d4", fontSize: 11 }}
                      tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                      domain={["auto", "auto"]}
                    />
                    <YAxis
                      yAxisId="fr"
                      orientation="right"
                      stroke="#10b981"
                      tick={{ fill: "#10b981", fontSize: 11 }}
                      tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                      domain={[0.7, 1.0]}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#020617",
                        borderColor: "#334155",
                        borderRadius: "0.5rem",
                        fontSize: "12px",
                      }}
                      formatter={(val: any, name: string) => {
                        if (name === "Contribution Margin") return [formatCurrency(val), name];
                        if (name === "Fill Rate") return [`${(val * 100).toFixed(1)}%`, name];
                        return [val, name];
                      }}
                    />
                    <Legend />
                    <Area
                      yAxisId="cm"
                      type="monotone"
                      dataKey="contribution_margin"
                      name="Contribution Margin"
                      stroke="#06b6d4"
                      strokeWidth={2.5}
                      fill="url(#cmGradient)"
                    />
                    <Line
                      yAxisId="fr"
                      type="monotone"
                      dataKey="fill_rate"
                      name="Fill Rate"
                      stroke="#10b981"
                      strokeWidth={2}
                      dot={{ r: 4, fill: "#10b981" }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
