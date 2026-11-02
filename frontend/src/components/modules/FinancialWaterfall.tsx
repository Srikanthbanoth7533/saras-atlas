"use client";

import React from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SimulationResponse } from "@/lib/types";
import { BarChart3, TrendingUp, DollarSign, ArrowDown, ShieldCheck } from "lucide-react";
import { formatCurrency, formatPercent } from "@/lib/utils";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

interface FinancialWaterfallProps {
  unmitigatedSim: SimulationResponse | null;
  mitigatedSim: SimulationResponse | null;
}

export function FinancialWaterfall({
  unmitigatedSim,
  mitigatedSim,
}: FinancialWaterfallProps) {
  // GAAP Unit CM Waterfall items
  const unitWaterfall = [
    { label: "Retail Gross Price", amount: 180.0, type: "revenue", note: "Hero SKU Apex Shell Jacket" },
    { label: "Inbound Landed COGS", amount: -45.15, type: "cost", note: "Factory FOB $42.00 + 7.5% Tariffs ($3.15)" },
    { label: "Pick & Pack 3PL Fee", amount: -4.50, type: "cost", note: "Warehouse pick/pack standard contract fee" },
    { label: "Outbound Shipping (Zone 2)", amount: -8.50, type: "cost", note: "Local parcel shipping under normal lanes" },
    { label: "Payment Processing Fee", amount: -5.52, type: "cost", note: "Stripe/Shopify (2.9% + $0.30/order)" },
    { label: "Allocated Paid Ad Spend", amount: -45.00, type: "cost", note: "Target Blended Customer Acquisition Cost (CAC)" },
    { label: "Net Unit Contribution Margin", amount: 71.33, type: "margin", note: "Healthy 39.63% GAAP Unit Margin" },
  ];

  // Disrupted Unit CM Waterfall (Zone 8 Cross-Country + Surcharge)
  const disruptedUnitWaterfall = [
    { label: "Retail Gross Price", amount: 180.0, type: "revenue" },
    { label: "Inbound Landed COGS", amount: -45.15, type: "cost" },
    { label: "Pick & Pack 3PL Fee", amount: -4.50, type: "cost" },
    { label: "Cross-Zone Outbound (Zone 8)", amount: -21.50, type: "cost", note: "Zone 8 ($16.80) + 28% Freight Surcharge" },
    { label: "Payment Processing Fee", amount: -5.52, type: "cost" },
    { label: "Allocated Paid Ad Spend", amount: -45.00, type: "cost" },
    { label: "Net Unit Margin (Disrupted)", amount: 58.33, type: "margin", note: "Margin compressed by 18.2%" },
  ];

  // Enterprise Aggregate P&L comparison data
  const baseCard = unmitigatedSim?.summary_scorecard;
  const mitCard = mitigatedSim?.summary_scorecard;

  const comparisonData = [
    {
      category: "Gross Revenue",
      "Unmitigated Disruption": baseCard?.net_revenue || 1071360,
      "ATLAS Mitigated Plan": mitCard?.net_revenue || 1425600,
    },
    {
      category: "Landed COGS",
      "Unmitigated Disruption": -(baseCard?.cogs_total || 268913),
      "ATLAS Mitigated Plan": -(mitCard?.cogs_total || 357860),
    },
    {
      category: "Total Freight",
      "Unmitigated Disruption": -(baseCard?.freight_total || 138420),
      "ATLAS Mitigated Plan": -(mitCard?.freight_total || 112840),
    },
    {
      category: "Allocated Ad Spend",
      "Unmitigated Disruption": -(baseCard?.allocated_ad_spend || 267840),
      "ATLAS Mitigated Plan": -(mitCard?.allocated_ad_spend || 234600),
    },
    {
      category: "Net CM ($)",
      "Unmitigated Disruption": baseCard?.net_contribution_margin || 328140,
      "ATLAS Mitigated Plan": mitCard?.net_contribution_margin || 618480,
    },
  ];

  return (
    <div className="space-y-6">
      {/* 1. Header & Overview */}
      <div className="command-panel rounded-xl p-5 border border-white/[0.08] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Financial Impact & Contribution Margin Waterfall
            </h2>
            <Badge variant="emerald" size="sm">GAAP PRECISION</Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic accounting model tracing revenue down through landed COGS, freight surcharges, and unit contribution margin.
          </p>
        </div>

        <div className="flex items-center gap-3 font-mono">
          <Badge variant="cyan" size="md">
            NORMAL UNIT CM: $71.33 (39.6%)
          </Badge>
          <Badge variant="rose" size="md">
            CROSS-ZONE UNIT CM: $58.33 (32.4%)
          </Badge>
        </div>
      </div>

      {/* 2. Enterprise Aggregate Comparison Chart */}
      <Card className="command-panel border-white/[0.08]">
        <CardHeader>
          <CardTitle>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <span>90-Day Enterprise Financial Waterfall: Unmitigated vs. ATLAS Mitigated Plan</span>
          </CardTitle>
          <Badge variant="emerald" size="sm">AGGREGATE 90-DAY WATERFALL</Badge>
        </CardHeader>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={comparisonData} margin={{ top: 20, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="category" stroke="#94A3B8" fontSize={11} tickLine={false} />
              <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} tickFormatter={(v) => `$${Math.abs(v) / 1000}k`} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0B0F17",
                  borderColor: "rgba(255,255,255,0.1)",
                  borderRadius: "8px",
                  fontFamily: "monospace",
                  fontSize: "12px",
                }}
                formatter={(val: any) => formatCurrency(Math.abs(Number(val)))}
              />
              <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
              <Bar dataKey="Unmitigated Disruption" fill="#EF4444" radius={[4, 4, 0, 0]} />
              <Bar dataKey="ATLAS Mitigated Plan" fill="#10B981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* 3. Unit Financial Waterfall Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Normal Unit Waterfall */}
        <Card className="command-panel border-cyan-500/30">
          <CardHeader>
            <CardTitle>
              <DollarSign className="w-4 h-4 text-cyan-400" />
              <span>Normal Local Fulfillment Unit Waterfall (Zone 2)</span>
            </CardTitle>
            <Badge variant="cyan" size="sm">BASELINE WATERFALL</Badge>
          </CardHeader>

          <div className="space-y-2">
            {unitWaterfall.map((item, idx) => (
              <div
                key={idx}
                className={`flex items-center justify-between p-2.5 rounded-lg font-mono text-xs ${
                  item.type === "margin"
                    ? "bg-emerald-950/70 border border-emerald-800/60 font-bold text-emerald-400"
                    : item.type === "revenue"
                    ? "bg-cyan-950/50 text-white font-bold"
                    : "bg-command-900/60 text-slate-300"
                }`}
              >
                <div>
                  <div className="font-semibold">{item.label}</div>
                  <div className="text-[10px] text-slate-400 font-sans">{item.note}</div>
                </div>
                <div className={`text-sm ${item.type === "margin" ? "text-emerald-400 font-black" : item.amount < 0 ? "text-rose-400" : "text-white"}`}>
                  {formatCurrency(item.amount)}
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Cross-Zone Disrupted Waterfall */}
        <Card className="command-panel border-rose-500/30">
          <CardHeader>
            <CardTitle>
              <ArrowDown className="w-4 h-4 text-rose-400" />
              <span className="text-rose-400">Out-of-Zone Cross-Country Waterfall (Zone 8)</span>
            </CardTitle>
            <Badge variant="rose" size="sm">DISRUPTED WATERFALL</Badge>
          </CardHeader>

          <div className="space-y-2">
            {disruptedUnitWaterfall.map((item, idx) => (
              <div
                key={idx}
                className={`flex items-center justify-between p-2.5 rounded-lg font-mono text-xs ${
                  item.type === "margin"
                    ? "bg-amber-950/70 border border-amber-800/60 font-bold text-amber-400"
                    : item.type === "revenue"
                    ? "bg-cyan-950/50 text-white font-bold"
                    : "bg-command-900/60 text-slate-300"
                }`}
              >
                <div>
                  <div className="font-semibold">{item.label}</div>
                  {item.note && <div className="text-[10px] text-slate-400 font-sans">{item.note}</div>}
                </div>
                <div className={`text-sm ${item.type === "margin" ? "text-amber-400 font-black" : item.amount < 0 ? "text-rose-400" : "text-white"}`}>
                  {formatCurrency(item.amount)}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
