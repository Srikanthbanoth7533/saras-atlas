"use client";

import React from "react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ActiveRisk } from "@/lib/types";
import { AlertOctagon, AlertTriangle, Activity, ArrowRight } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

interface RiskMonitoringProps {
  risks: ActiveRisk[];
  onSimulateRisk?: (risk: ActiveRisk) => void;
}

/**
 * Computes estimated financial exposure across various risk payload formats.
 */
function getRiskExposure(risk: ActiveRisk): number {
  if (typeof risk.financial_exposure_estimate === "number") {
    return risk.financial_exposure_estimate;
  }
  if (typeof risk.estimated_revenue_exposure === "number") {
    return risk.estimated_revenue_exposure;
  }
  if (typeof risk.estimated_monthly_freight_inflation === "number") {
    return risk.estimated_monthly_freight_inflation;
  }
  if (typeof risk.cost_delta_per_unit === "number") {
    return risk.cost_delta_per_unit * 10000;
  }
  return 0;
}

/**
 * Safely resolves impacted entity tags with fallbacks for SKU codes, warehouses, and entity IDs.
 */
function getImpactedEntities(risk: ActiveRisk): string[] {
  if (Array.isArray(risk.impacted_entities) && risk.impacted_entities.length > 0) {
    return risk.impacted_entities;
  }
  const tags: string[] = [];
  if (risk.entity_id) {
    tags.push(risk.entity_id);
  }
  if (risk.destination_warehouse && !tags.includes(risk.destination_warehouse)) {
    tags.push(risk.destination_warehouse);
  }
  if (risk.affected_warehouse && !tags.includes(risk.affected_warehouse)) {
    tags.push(risk.affected_warehouse);
  }
  if (Array.isArray(risk.vulnerable_skus)) {
    for (const item of risk.vulnerable_skus.slice(0, 3)) {
      const code = item?.sku_code;
      if (code && !tags.includes(code)) {
        tags.push(code);
      }
    }
  }
  return tags.length > 0 ? tags : ["Vanguard Network"];
}

/**
 * Resolves deterministic recommended action playbooks when missing from API response.
 */
function getRecommendedAction(risk: ActiveRisk): string {
  if (risk.recommended_action && risk.recommended_action.trim().length > 0) {
    return risk.recommended_action;
  }
  if (risk.risk_type === "SUPPLIER_INBOUND_DELAY") {
    return "Initiate emergency air freight allocation (1,500 units) and Reno buffer replenishment.";
  }
  if (risk.risk_type === "CARRIER_LANE_SURCHARGE") {
    return "Audit carrier force majeure clauses and shift volume to regional parcel carriers.";
  }
  if (risk.risk_type === "OUT_OF_ZONE_EXPEDITED_DRAIN") {
    return "Throttle ad spend on western regional campaigns (-18%) to prevent cross-zone margin drain.";
  }
  if (risk.severity === "CRITICAL") {
    return "Deploy immediate executive mitigation protocol and buffer reallocation.";
  }
  return "Monitor carrier SLA telemetry and review secondary fulfillment lanes.";
}

export function RiskMonitoring({ risks = [], onSimulateRisk }: RiskMonitoringProps) {
  const safeRisks = Array.isArray(risks) ? risks : [];
  const criticalCount = safeRisks.filter((r) => r.severity === "CRITICAL").length;
  const warningCount = safeRisks.filter((r) => r.severity === "WARNING" || r.severity === "HIGH").length;
  const totalExposure = safeRisks.reduce((sum, r) => sum + getRiskExposure(r), 0);

  return (
    <div className="space-y-6">
      {/* 1. Risk Sentinel Header Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="command-panel rounded-xl p-4 border border-rose-500/40">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
            Critical Disruption Sentinels
          </span>
          <div className="flex items-center gap-2 mt-2">
            <AlertOctagon className="w-5 h-5 text-rose-400 animate-pulse" />
            <span className="text-2xl font-bold font-mono text-rose-400">{criticalCount} Active</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Requires immediate executive intervention</p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-amber-500/40">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
            Operational Warnings
          </span>
          <div className="flex items-center gap-2 mt-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span className="text-2xl font-bold font-mono text-amber-400">{warningCount} Warnings</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Elevated strain on secondary transit corridors</p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-white/[0.08]">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
            Cumulative Financial Exposure
          </span>
          <div className="flex items-center gap-1.5 mt-2 text-2xl font-bold font-mono text-white">
            <span>{formatCurrency(totalExposure)}</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Estimated unmitigated downside across active alerts</p>
        </div>

        <div className="command-panel rounded-xl p-4 border border-white/[0.08]">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
            Monitoring Engine
          </span>
          <div className="flex items-center gap-2 mt-2 text-sm font-bold text-cyan-400 font-mono">
            <Activity className="w-4 h-4 text-cyan-400" />
            <span>OperationalRiskSentinel</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Continuous multi-echelon network scan</p>
        </div>
      </div>

      {/* 2. Prioritized Sentinel Alerts List */}
      <div className="space-y-4">
        <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Active Operational Risk Sentinels & Recommended Playbooks</span>
          <span className="h-px flex-1 bg-white/[0.08]" />
        </h3>

        {safeRisks.map((risk) => {
          const isCritical = risk.severity === "CRITICAL";
          const exposure = getRiskExposure(risk);
          const entities = getImpactedEntities(risk);
          const categoryText = risk.category || risk.risk_type || "SUPPLY_CHAIN_RISK";
          const descriptionText = risk.description || risk.summary || "Operational anomaly detected.";
          const actionText = getRecommendedAction(risk);

          return (
            <Card
              key={risk.risk_id}
              className={`command-panel border ${
                isCritical ? "border-rose-500/40 hover:border-rose-500/70" : "border-amber-500/40 hover:border-amber-500/70"
              } transition-all`}
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div className="space-y-2 flex-1">
                  <div className="flex items-center gap-2.5 flex-wrap">
                    <Badge variant={isCritical ? "rose" : "amber"} size="sm">
                      {risk.severity}
                    </Badge>
                    <span className="text-xs font-mono text-slate-400">{categoryText}</span>
                    <span className="text-xs font-mono text-slate-500">•</span>
                    <span className="text-xs font-mono text-slate-400 font-semibold">{risk.risk_id}</span>
                  </div>

                  <h4 className="text-base font-bold text-white">{risk.title}</h4>
                  <p className="text-xs text-slate-300 leading-relaxed max-w-4xl">{descriptionText}</p>

                  <div className="flex items-center gap-4 flex-wrap pt-1 text-xs">
                    <div className="flex items-center gap-1.5 font-mono">
                      <span className="text-slate-400">Financial Exposure:</span>
                      <span className="font-bold text-rose-400">
                        {formatCurrency(exposure)}
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5 font-mono">
                      <span className="text-slate-400">Entities Impacted:</span>
                      <div className="flex gap-1 flex-wrap">
                        {entities.map((e) => (
                          <span
                            key={e}
                            className="bg-command-800 border border-white/[0.08] px-1.5 py-0.5 rounded text-[11px] text-cyan-300"
                          >
                            {e}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-command-900/90 border border-white/[0.06] rounded-xl p-3.5 lg:w-80 flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-mono uppercase text-slate-400 tracking-wider">
                      Recommended Action
                    </span>
                    <p className="text-xs text-slate-200 mt-1 font-medium">{actionText}</p>
                  </div>

                  {onSimulateRisk && (
                    <button
                      onClick={() => onSimulateRisk(risk)}
                      className="mt-3 px-3 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-800/60 text-cyan-300 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer"
                    >
                      <span>Simulate Mitigation</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
