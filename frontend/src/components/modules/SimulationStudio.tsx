"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SliderControl } from "@/components/ui/SliderControl";
import { StatCard } from "@/components/ui/StatCard";
import { SimulationRequest, SimulationResponse } from "@/lib/types";
import { Sliders, Play, RotateCcw, TrendingUp, DollarSign, Package, Clock, Zap, AlertTriangle } from "lucide-react";
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

interface SimulationStudioProps {
  onRunSimulation: (req: SimulationRequest) => Promise<SimulationResponse>;
  simulationResult: SimulationResponse | null;
  isLoading?: boolean;
}

export function SimulationStudio({
  onRunSimulation,
  simulationResult,
  isLoading = false,
}: SimulationStudioProps) {
  // Shock sliders state (Defaults as specified in prompt)
  const [supplierDelay, setSupplierDelay] = useState(21);
  const [freightSurcharge, setFreightSurcharge] = useState(28);
  const [demandSurge, setDemandSurge] = useState(45);
  const [horizonDays, setHorizonDays] = useState(90);

  // Mitigation levers state
  const [airUnits, setAirUnits] = useState(0);
  const [transferUnits, setTransferUnits] = useState(0);
  const [adThrottle, setAdThrottle] = useState(0);

  const handleSimulate = async () => {
    const req: SimulationRequest = {
      scenario_name: `Interactive Simulation (Delay: ${supplierDelay}d, Surcharge: ${freightSurcharge}%, Surge: ${demandSurge}%)`,
      horizon_days: horizonDays,
      shocks: {
        supplier_delays: [{ po_number: "PO-9012", delay_days: supplierDelay }],
        freight_surcharges: [{ lane_id: "lane_east_coast_parcel", surcharge_percentage: freightSurcharge / 100 }],
        demand_elasticities: [{ sku_code: "APEX-JKT", demand_multiplier: 1.0 + demandSurge / 100, duration_days: 30 }],
      },
      mitigations: {
        emergency_air_freight_units: airUnits,
        inter_warehouse_transfer_units: transferUnits,
        ad_spend_throttle_percentage: adThrottle / 100,
      },
    };
    await onRunSimulation(req);
  };

  const handleApplyOptimalMitigation = () => {
    setAirUnits(1500);
    setTransferUnits(600);
    setAdThrottle(18);
  };

  const handleResetToBaseline = () => {
    setSupplierDelay(0);
    setFreightSurcharge(0);
    setDemandSurge(0);
    setAirUnits(0);
    setTransferUnits(0);
    setAdThrottle(0);
  };

  // Build timeseries chart data from simulation result
  const chartData = simulationResult
    ? simulationResult.daily_timeseries.revenue.map((rev, idx) => ({
        day: `D${idx + 1}`,
        Revenue: rev,
        Margin: simulationResult.daily_timeseries.contribution_margin[idx] || 0,
        Cash: simulationResult.daily_timeseries.cash_balance[idx] || 0,
      }))
    : [];

  const scorecard = simulationResult?.summary_scorecard;

  return (
    <div className="space-y-6">
      {/* 1. Control Studio Header & Action Bar */}
      <div className="command-panel rounded-xl p-5 border border-white/[0.08] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <Sliders className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-white font-mono uppercase tracking-wider">
              Multi-Echelon Scenario Simulation Studio
            </h2>
            <Badge variant="cyan" size="sm">
              90-DAY DISCRETE DIFFERENCE ENGINE
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Simulate non-linear shock cascades across supplier lead times, freight lanes, and viral demand spikes.
          </p>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          <button
            onClick={handleApplyOptimalMitigation}
            className="px-3 py-1.5 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-700/60 text-indigo-300 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <Zap className="w-3.5 h-3.5 text-indigo-400" />
            <span>Preset: ATLAS Optimal</span>
          </button>
          <button
            onClick={handleResetToBaseline}
            className="px-3 py-1.5 rounded-lg bg-command-850 hover:bg-command-800 border border-white/[0.08] text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Levers</span>
          </button>
          <button
            onClick={handleSimulate}
            disabled={isLoading}
            className="px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider shadow-[0_0_20px_rgba(6,182,212,0.4)] flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            <span>{isLoading ? "Simulating..." : "Execute Simulation"}</span>
          </button>
        </div>
      </div>

      {/* 2. Interactive Shock & Mitigation Sliders Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Shocks Panel */}
        <Card className="command-panel border-rose-500/30">
          <CardHeader>
            <CardTitle>
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              <span className="text-rose-400">Exogenous Shock Levers</span>
            </CardTitle>
            <Badge variant="rose" size="sm">INPUT SHOCKS</Badge>
          </CardHeader>

          <div className="space-y-4">
            <SliderControl
              label="Supplier Shipment Delay (PO-9012)"
              value={supplierDelay}
              min={0}
              max={60}
              unit=" days"
              defaultValue={21}
              description="Port berthing delay for 10,000 units on vessel Ever Forward"
              onChange={setSupplierDelay}
              accentColor="rose"
            />

            <SliderControl
              label="Freight Congestion Surcharge"
              value={freightSurcharge}
              min={0}
              max={100}
              unit="%"
              defaultValue={28}
              description="Emergency carrier surcharge on Eastern US parcel corridors"
              onChange={setFreightSurcharge}
              accentColor="amber"
            />

            <SliderControl
              label="Demand Surge Multiplier"
              value={demandSurge}
              min={0}
              max={100}
              unit="%"
              defaultValue={45}
              description="Viral social media campaign demand spike on Apex Jacket (30 days)"
              onChange={setDemandSurge}
              accentColor="cyan"
            />
          </div>
        </Card>

        {/* Mitigations Panel */}
        <Card className="command-panel border-emerald-500/30">
          <CardHeader>
            <CardTitle>
              <Zap className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-400">Prescriptive Mitigation Levers</span>
            </CardTitle>
            <Badge variant="emerald" size="sm">CORRECTIVE ACTIONS</Badge>
          </CardHeader>

          <div className="space-y-4">
            <SliderControl
              label="Emergency Air Freight (Saigon)"
              value={airUnits}
              min={0}
              max={3000}
              step={100}
              unit=" units"
              defaultValue={1500}
              description="Expedited production & air wire from Vietnam backup factory ($12.50/unit)"
              onChange={setAirUnits}
              accentColor="cyan"
            />

            <SliderControl
              label="Inter-Warehouse Transfer (East → West)"
              value={transferUnits}
              min={0}
              max={800}
              step={50}
              unit=" units"
              defaultValue={600}
              description="Ground LTL stock rebalancing from Allentown to Reno ($3.20/unit)"
              onChange={setTransferUnits}
              accentColor="emerald"
            />

            <SliderControl
              label="Ad Spend Throttle"
              value={adThrottle}
              min={0}
              max={35}
              unit="%"
              defaultValue={18}
              description="Dampen paid customer acquisition to avoid burning ad spend on stockouts"
              onChange={setAdThrottle}
              accentColor="indigo"
            />
          </div>
        </Card>
      </div>

      {/* 3. Real-Time Simulation Financial Scorecard */}
      {scorecard && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400">
              Live Simulation Financial Scorecard (Executed in {simulationResult?.execution_duration_ms} ms)
            </h3>
            <span className="text-xs font-mono text-cyan-400 font-bold">
              Status: {scorecard.stockout_days === 0 ? "RESILIENT (0 DAYS LOST)" : `${scorecard.stockout_days} DAYS OF STOCKOUT`}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            <StatCard
              title="Net Gross Revenue"
              value={formatCurrency(scorecard.net_revenue)}
              subtext="Full 90-day period"
              variant="cyan"
            />
            <StatCard
              title="Net Contribution Margin"
              value={formatCurrency(scorecard.net_contribution_margin)}
              subtext={`${formatPercent(scorecard.contribution_margin_pct)} margin`}
              variant="emerald"
            />
            <StatCard
              title="Landed COGS"
              value={formatCurrency(scorecard.cogs_total)}
              subtext="Base + tariffs"
              variant="default"
            />
            <StatCard
              title="Total Freight Cost"
              value={formatCurrency(scorecard.freight_total)}
              subtext="Zone 2 + Zone 8"
              variant="amber"
            />
            <StatCard
              title="Orders Fulfilled"
              value={formatNumber(scorecard.total_orders_fulfilled)}
              subtext={`${formatNumber(scorecard.unfulfilled_lost_orders)} lost`}
              variant={scorecard.unfulfilled_lost_orders === 0 ? "emerald" : "rose"}
            />
            <StatCard
              title="Capital Required"
              value={formatCurrency(scorecard.working_capital_required)}
              subtext="Self-funding liquidity"
              variant="cyan"
            />
          </div>
        </div>
      )}

      {/* 4. 90-Day Trajectory Area Chart */}
      {chartData.length > 0 && (
        <Card className="command-panel border-white/[0.08]">
          <CardHeader>
            <CardTitle>
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              <span>90-Day Trajectory: Daily Revenue, Contribution Margin & Cash Liquidity</span>
            </CardTitle>
            <Badge variant="cyan" size="sm">VECTORIZED DISCRETE TRAJECTORY</Badge>
          </CardHeader>

          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRev" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#06B6D4" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorMargin" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="day" stroke="#64748B" fontSize={10} tickLine={false} interval={9} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} tickFormatter={(v) => `$${v / 1000}k`} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0B0F17",
                    borderColor: "rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                    fontFamily: "monospace",
                    fontSize: "12px",
                  }}
                  formatter={(val: any) => formatCurrency(Number(val))}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
                <Area type="monotone" dataKey="Revenue" stroke="#06B6D4" strokeWidth={2} fillOpacity={1} fill="url(#colorRev)" />
                <Area type="monotone" dataKey="Margin" stroke="#10B981" strokeWidth={2} fillOpacity={1} fill="url(#colorMargin)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}
    </div>
  );
}
