"use client";

import React from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ActiveRisk } from "@/lib/types";
import { AlertOctagon, AlertTriangle, ShieldAlert, ArrowRight, DollarSign, Activity } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

interface RiskMonitoringProps {
  risks: ActiveRisk[];
  onSimulateRisk?: (risk: ActiveRisk) => void;
}

export function RiskMonitoring({ risks, onSimulateRisk }: RiskMonitoringProps) {
  const criticalCount = risks.filter((r) => r.severity === "CRITICAL").length;
  const warningCount = risks.filter((r) => r.severity === "WARNING").length;
  const totalExposure = risks.reduce((sum, r) => sum + (r.financial_exposure_estimate || 0), 0);

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

        {risks.map((risk) => {
          const isCritical = risk.severity === "CRITICAL";

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
                    <span className="text-xs font-mono text-slate-400">{risk.category}</span>
                    <span className="text-xs font-mono text-slate-500">•</span>
                    <span className="text-xs font-mono text-slate-400 font-semibold">{risk.risk_id}</span>
                  </div>

                  <h4 className="text-base font-bold text-white">{risk.title}</h4>
                  <p className="text-xs text-slate-300 leading-relaxed max-w-4xl">{risk.description}</p>

                  <div className="flex items-center gap-4 flex-wrap pt-1 text-xs">
                    <div className="flex items-center gap-1.5 font-mono">
                      <span className="text-slate-400">Financial Exposure:</span>
                      <span className="font-bold text-rose-400">
                        {formatCurrency(risk.financial_exposure_estimate)}
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5 font-mono">
                      <span className="text-slate-400">Entities Impacted:</span>
                      <div className="flex gap-1">
                        {risk.impacted_entities.map((e) => (
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
                    <p className="text-xs text-slate-200 mt-1 font-medium">{risk.recommended_action}</p>
                  </div>

                  {onSimulateRisk && (
                    <button
                      onClick={() => onSimulateRisk(risk)}
                      className="mt-3 px-3 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-800/60 text-cyan-300 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all"
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
