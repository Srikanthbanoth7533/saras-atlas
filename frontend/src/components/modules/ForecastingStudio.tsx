"use client";

import React, { useState, useEffect } from "react";
import {
  TrendingUp,
  Activity,
  AlertCircle,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  BarChart2,
  RefreshCw,
  Clock,
  ShieldAlert,
} from "lucide-react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { fetchForecastingEvaluation } from "@/lib/api";
import { ForecastingEvaluationResponse, ModelEvaluationScore } from "@/lib/types";

export default function ForecastingStudio() {
  const [seriesType, setSeriesType] = useState<"DAILY_DEMAND" | "LEAD_TIME_DAYS">("DAILY_DEMAND");
  const [horizonDays, setHorizonDays] = useState(30);
  const [data, setData] = useState<ForecastingEvaluationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadForecast = async (type: string, horizon: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchForecastingEvaluation(type, horizon);
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load forecasting evaluation.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadForecast(seriesType, horizonDays);
  }, [seriesType, horizonDays]);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-800/40 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg">
                <TrendingUp className="w-6 h-6" />
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                Advanced Statistical & ML Forecasting Studio
              </h2>
              <Badge variant="cyan" className="text-xs">
                Held-Out Empirical Evaluation (78/22 Split)
              </Badge>
            </div>
            <p className="text-sm text-slate-300 max-w-3xl">
              Lightweight time-series models (Holt-Winters, Ridge Autoregressor, Moving Average)
              evaluated strictly against held-out empirical data with calibrated 80% and 95%
              prediction intervals and statistical drift detection.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => loadForecast(seriesType, horizonDays)}
              disabled={loading}
              className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center space-x-1.5 transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
              <span>Refit Models</span>
            </button>
          </div>
        </div>
      </div>

      {/* Series Selector & Controls */}
      <Card className="p-4 bg-slate-900/90 border-slate-800">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">
              Target Series:
            </span>
            <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
              <button
                onClick={() => setSeriesType("DAILY_DEMAND")}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  seriesType === "DAILY_DEMAND"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Omnichannel Demand (Units)
              </button>
              <button
                onClick={() => setSeriesType("LEAD_TIME_DAYS")}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  seriesType === "LEAD_TIME_DAYS"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Supplier Lead Time (Days)
              </button>
            </div>
          </div>

          <div className="flex items-center space-x-3 text-xs text-slate-300">
            <span className="text-slate-400 font-medium">Horizon:</span>
            {[14, 30, 45, 60].map((h) => (
              <button
                key={h}
                onClick={() => setHorizonDays(h)}
                className={`px-2.5 py-1 rounded text-xs transition-colors ${
                  horizonDays === h
                    ? "bg-slate-700 text-white font-bold"
                    : "bg-slate-950 hover:bg-slate-800 text-slate-400"
                }`}
              >
                +{h} Days
              </button>
            ))}
          </div>
        </div>
      </Card>

      {error && (
        <div className="p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="p-12 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <span>Fitting Holt-Winters & Ridge models against held-out partition...</span>
        </div>
      )}

      {data && !loading && (
        <>
          {/* Top 4 KPI Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title="Best Evaluated Model"
              value={data.best_model_name.split("(")[0]}
              subtext="Selected by Lowest WAPE"
              variant="cyan"
            />
            <StatCard
              title="Held-Out WAPE Error"
              value={`${data.models_evaluated.find((m) => m.is_best_model)?.wape.toFixed(2)}%`}
              delta={{
                value: `MAE: ${data.models_evaluated.find((m) => m.is_best_model)?.mae.toFixed(1)} units`,
                isPositive: true,
                isGood: true,
              }}
              variant="emerald"
            />
            <StatCard
              title="Statistical Drift Status"
              value={data.drift_analysis.drift_severity}
              subtext={`Z-Shift: ${data.drift_analysis.z_score_shift.toFixed(2)}σ`}
              variant={data.drift_analysis.drift_detected ? "amber" : "emerald"}
            />
            <StatCard
              title="Validation Partition"
              value={`${data.train_periods}d Train / ${data.test_periods}d Test`}
              subtext="Out-of-Time Held-Out Split"
              variant="default"
            />
          </div>

          {/* Interactive Recharts Trajectory with Prediction Intervals */}
          <Card className="p-6 bg-slate-900/90 border-slate-800">
            <CardHeader className="p-0 pb-4 mb-4 border-b border-slate-800 flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-base font-bold text-white flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-indigo-400" />
                  <span>Historical Actuals vs Forecast with 80% & 95% Confidence Intervals</span>
                </CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Days 1–90 show historical observed data; Days 91–{90 + data.forecast_horizon} show
                  the projected forward horizon with expanding uncertainty bounds.
                </p>
              </div>
              <Badge variant="cyan" className="text-xs font-mono">
                Model: {data.best_model_name}
              </Badge>
            </CardHeader>

            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart
                  data={data.forecast_trajectory}
                  margin={{ top: 10, right: 20, left: 10, bottom: 0 }}
                >
                  <defs>
                    <linearGradient id="band95" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0.02} />
                    </linearGradient>
                    <linearGradient id="band80" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#818cf8" stopOpacity={0.05} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
                  <XAxis
                    dataKey="period"
                    stroke="#94a3b8"
                    fontSize={11}
                    tickFormatter={(val) => `D${val}`}
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} domain={["auto", "auto"]} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      borderColor: "#334155",
                      fontSize: "12px",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "12px" }} />

                  {/* 95% Confidence Band */}
                  <Area
                    type="monotone"
                    dataKey="upper_95"
                    stroke="none"
                    fill="url(#band95)"
                    name="95% Upper Bound"
                  />
                  <Area
                    type="monotone"
                    dataKey="lower_95"
                    stroke="none"
                    fill="#0f172a"
                    name="95% Lower Bound"
                  />

                  {/* 80% Confidence Band */}
                  <Area
                    type="monotone"
                    dataKey="upper_80"
                    stroke="none"
                    fill="url(#band80)"
                    name="80% Upper Bound"
                  />
                  <Area
                    type="monotone"
                    dataKey="lower_80"
                    stroke="none"
                    fill="#0f172a"
                    name="80% Lower Bound"
                  />

                  {/* Predicted Curve */}
                  <Line
                    type="monotone"
                    dataKey="predicted"
                    stroke="#818cf8"
                    strokeWidth={2}
                    dot={false}
                    name="Model Forecast"
                  />

                  {/* Actual Historical Curve */}
                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#38bdf8"
                    strokeWidth={2}
                    dot={false}
                    name="Historical Observed"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Model Comparison Scorecard & Drift Monitor */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left 2 Cols: Model Scorecard Table */}
            <div className="lg:col-span-2">
              <Card className="p-6 bg-slate-900/90 border-slate-800">
                <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                  <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                    <BarChart2 className="w-4 h-4 text-indigo-400" />
                    <span>Held-Out Empirical Model Evaluation Scorecard</span>
                  </CardTitle>
                </CardHeader>
                <p className="text-xs text-slate-400 mb-4">
                  Models trained on Days 1–{data.train_periods} and evaluated strictly against held-out
                  Days {data.train_periods + 1}–{data.train_periods + data.test_periods}.
                </p>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 font-mono">
                        <th className="pb-2.5">Candidate Model</th>
                        <th className="pb-2.5">MAE</th>
                        <th className="pb-2.5">RMSE</th>
                        <th className="pb-2.5">MAPE</th>
                        <th className="pb-2.5">WAPE</th>
                        <th className="pb-2.5">Latency</th>
                        <th className="pb-2.5 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60 font-mono">
                      {data.models_evaluated.map((m: ModelEvaluationScore, idx: number) => (
                        <tr
                          key={idx}
                          className={m.is_best_model ? "bg-indigo-950/30 text-indigo-200" : "text-slate-300"}
                        >
                          <td className="py-3 font-sans font-medium text-white flex items-center space-x-2">
                            {m.is_best_model && (
                              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                            )}
                            <span>{m.model_name}</span>
                          </td>
                          <td className="py-3">{m.mae.toFixed(1)}</td>
                          <td className="py-3">{m.rmse.toFixed(1)}</td>
                          <td className="py-3">{m.mape.toFixed(2)}%</td>
                          <td className="py-3 font-bold text-emerald-400">{m.wape.toFixed(2)}%</td>
                          <td className="py-3 text-slate-400">{m.fit_duration_ms.toFixed(1)} ms</td>
                          <td className="py-3 text-right">
                            {m.is_best_model ? (
                              <Badge variant="emerald" className="text-[10px]">
                                Selected
                              </Badge>
                            ) : (
                              <Badge variant="default" className="text-[10px]">
                                Baseline
                              </Badge>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </div>

            {/* Right Col: Statistical Drift Sentinel */}
            <div>
              <Card className="p-6 bg-slate-900/90 border-slate-800 h-full flex flex-col justify-between">
                <div>
                  <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                    <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                      <ShieldAlert className="w-4 h-4 text-amber-400" />
                      <span>Kolmogorov-Smirnov Drift Monitor</span>
                    </CardTitle>
                  </CardHeader>
                  <p className="text-xs text-slate-400 mb-4">
                    Two-sample statistical hypothesis testing comparing early baseline vs late observations.
                  </p>

                  <div className="space-y-3 text-xs">
                    <div className="p-3 bg-slate-950/70 border border-slate-800 rounded-lg space-y-1">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Drift Detected:</span>
                        <span
                          className={`font-bold ${
                            data.drift_analysis.drift_detected ? "text-amber-400" : "text-emerald-400"
                          }`}
                        >
                          {data.drift_analysis.drift_detected ? "YES (Warning)" : "NO (Stable)"}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Severity:</span>
                        <span className="font-mono text-slate-200">
                          {data.drift_analysis.drift_severity}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">KS Statistic:</span>
                        <span className="font-mono text-slate-200">
                          {data.drift_analysis.ks_statistic.toFixed(3)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">P-Value:</span>
                        <span className="font-mono text-slate-200">
                          {data.drift_analysis.p_value.toFixed(4)}
                        </span>
                      </div>
                    </div>

                    <div className="p-3 bg-slate-950/50 border border-slate-800/80 rounded-lg text-slate-300 leading-relaxed text-[11px]">
                      {data.drift_analysis.message}
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center space-x-1.5">
                  <Clock className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                  <span>Cadence: {data.drift_analysis.recommended_retraining_cadence}</span>
                </div>
              </Card>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
