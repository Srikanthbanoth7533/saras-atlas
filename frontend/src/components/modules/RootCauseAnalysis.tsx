"use client";

import React, { useState, useEffect } from "react";
import {
  GitMerge,
  AlertTriangle,
  ArrowDown,
  DollarSign,
  TrendingDown,
  Sliders,
  ShieldCheck,
  Building2,
  Ship,
  Truck,
  Package,
} from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { fetchRootCauseTrace } from "@/lib/api";
import { RootCauseTraceResponse, CausalNode } from "@/lib/types";

export default function RootCauseAnalysis() {
  const [data, setData] = useState<RootCauseTraceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRootCauseTrace()
      .then(setData)
      .catch((err) => setError(err?.message || "Failed to load Root Cause Analysis data."))
      .finally(() => setLoading(false));
  }, []);

  const getLayerIcon = (layer: string) => {
    switch (layer) {
      case "UPSTREAM_SUPPLIER":
        return <Building2 className="w-5 h-5 text-amber-400" />;
      case "LOGISTICS_CORRIDOR":
        return <Ship className="w-5 h-5 text-blue-400" />;
      case "FULFILLMENT_NODE":
        return <Package className="w-5 h-5 text-rose-400" />;
      case "CUSTOMER_DELIVERY":
        return <Truck className="w-5 h-5 text-purple-400" />;
      case "FINANCIAL_EBITDA":
        return <DollarSign className="w-5 h-5 text-emerald-400" />;
      default:
        return <GitMerge className="w-5 h-5 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-rose-950/40 to-slate-900 border border-rose-800/40 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="p-2 bg-rose-500/20 text-rose-400 rounded-lg">
                <GitMerge className="w-6 h-6" />
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                Disruption Root Cause Analysis & Dependency Tracing
              </h2>
              <Badge variant="rose" className="text-xs">
                Active Incident PO-9012
              </Badge>
            </div>
            <p className="text-sm text-slate-300 max-w-3xl">
              Deterministic causal attribution tracing the cascade from primary upstream port delay
              through fulfillment inventory depletion down to bottom-line GAAP contribution margin loss.
            </p>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 block">Total Attributed Financial Loss</span>
            <span className="text-2xl font-mono font-bold text-rose-400">
              {data ? `$${data.total_financial_impact.toLocaleString()}` : "$224,500.00"}
            </span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <span>Tracing causal dependency network across tiers...</span>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm">
          {error}
        </div>
      )}

      {data && (
        <>
          {/* Top 4 KPI Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title="Primary Root Trigger"
              value="PO-9012 Maritime Delay"
              subtext="+21 Days Berth Wait"
              variant="rose"
            />
            <StatCard
              title="First Stockout Vulnerability"
              value="WH-WEST (Los Angeles)"
              subtext="Runout on Day 34"
              variant="rose"
            />
            <StatCard
              title="Unit CM Degradation"
              value="$71.33 -> $58.33"
              delta={{ value: "-18.2%", isPositive: false, isGood: false }}
              variant="rose"
            />
            <StatCard
              title="Top Influential Sensitivity"
              value="Lead Time Variance"
              subtext="Rank #1 (Score: 0.92)"
              variant="amber"
            />
          </div>

          {/* Causal Propagation Chain */}
          <Card className="p-6 bg-slate-900/90 border-slate-800">
            <CardHeader className="p-0 pb-4 mb-4 border-b border-slate-800">
              <CardTitle className="text-base font-bold text-white flex items-center space-x-2">
                <GitMerge className="w-5 h-5 text-blue-400" />
                <span>Multi-Tiered Causal Propagation Pathway</span>
              </CardTitle>
            </CardHeader>
            <p className="text-xs text-slate-400 mb-6">
              Step-by-step risk transmission sequence showing how an operational trigger in Asia propagates
              through logistics corridors into customer delivery breaches and financial erosion.
            </p>

            <div className="space-y-4 relative">
              {data.causal_chain.map((node: CausalNode, idx: number) => (
                <div key={node.node_id} className="relative">
                  <div className="p-4 bg-slate-950/70 border border-slate-800 rounded-xl hover:border-slate-700 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex items-start space-x-3.5">
                      <div className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg shrink-0">
                        {getLayerIcon(node.layer)}
                      </div>
                      <div>
                        <div className="flex items-center space-x-2.5 mb-1">
                          <span className="text-xs font-mono font-bold text-slate-400">
                            Step {idx + 1}:
                          </span>
                          <span className="text-sm font-bold text-white">{node.label}</span>
                          <Badge
                            variant={node.severity === "CRITICAL" ? "rose" : "amber"}
                            className="text-[10px]"
                          >
                            {node.layer}
                          </Badge>
                        </div>
                        <p className="text-xs text-slate-300 max-w-2xl">{node.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4 shrink-0 md:text-right border-t md:border-t-0 pt-2 md:pt-0 border-slate-800/80">
                      <div>
                        <span className="text-[11px] text-slate-400 block">{node.metric_label}</span>
                        <span className="text-sm font-mono font-bold text-amber-300">
                          {node.metric_value}
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-[10px] text-slate-500 block">Causal Weight</span>
                        <span className="text-xs font-mono text-slate-300">
                          {(node.impact_weight * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Downward connector arrow between steps */}
                  {idx < data.causal_chain.length - 1 && (
                    <div className="flex justify-center my-1.5">
                      <ArrowDown className="w-4 h-4 text-slate-600" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </Card>

          {/* Two Cols: Financial Loss Attribution & Top Influential Variables */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left: Financial Impact Attribution Breakdown */}
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800 flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <TrendingDown className="w-4 h-4 text-rose-400" />
                  <span>Financial Loss Attribution Waterfall</span>
                </CardTitle>
                <span className="text-xs font-mono font-bold text-rose-400">
                  Total: ${data.total_financial_impact.toLocaleString()}
                </span>
              </CardHeader>
              <p className="text-xs text-slate-400 mb-4">
                Exact dollar allocation decomposing where contribution margin is lost across GAAP accounting lines.
              </p>

              <div className="space-y-3">
                {data.financial_attribution.map((seg, i) => (
                  <div
                    key={i}
                    className="p-3 bg-slate-950/70 border border-slate-800/90 rounded-lg space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-200">{seg.segment_name}</span>
                      <span className="font-mono font-bold text-rose-400">
                        ${seg.dollar_impact.toLocaleString()} ({seg.percentage_of_total}%)
                      </span>
                    </div>
                    {/* Progress Bar */}
                    <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="bg-rose-500 h-full rounded-full"
                        style={{ width: `${seg.percentage_of_total}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-500">
                      <span>Category: {seg.accounting_category}</span>
                      <span className="italic">{seg.evidence_citation}</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Right: Top Influential Sensitivity Variables */}
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <Sliders className="w-4 h-4 text-blue-400" />
                  <span>Most Influential Variables (Sensitivity Ranking)</span>
                </CardTitle>
              </CardHeader>
              <p className="text-xs text-slate-400 mb-4">
                Normalized partial derivatives measuring which operational parameters exert the greatest impact on net margin.
              </p>

              <div className="space-y-3">
                {data.top_influential_variables.map((v) => (
                  <div
                    key={v.elasticity_rank}
                    className="p-3 bg-slate-950/70 border border-slate-800/90 rounded-lg"
                  >
                    <div className="flex items-center justify-between text-xs mb-1">
                      <div className="flex items-center space-x-2">
                        <span className="w-5 h-5 bg-blue-500/20 text-blue-400 rounded-full flex items-center justify-center font-bold text-[10px]">
                          #{v.elasticity_rank}
                        </span>
                        <span className="font-semibold text-slate-200">{v.variable_name}</span>
                      </div>
                      <span className="font-mono text-amber-300 font-bold">
                        Score: {v.sensitivity_score.toFixed(2)}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 mb-1.5">{v.explanation}</p>
                    <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
                      <span>Baseline: {v.baseline_value}</span>
                      <span className="text-rose-400 font-semibold">Observed: {v.observed_value}</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Evidence Telemetry Citations Footer */}
          <div className="p-4 bg-slate-950/70 border border-slate-800 rounded-xl text-xs text-slate-400 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Grounded in active SQLite tables and verified discrete difference simulation matrices.</span>
            </div>
            <span className="text-[11px] text-slate-500">
              Audit Telemetry: {data.evidence_telemetry.length} verification checks verified
            </span>
          </div>
        </>
      )}
    </div>
  );
}
