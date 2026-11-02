"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Header } from "@/components/layout/Header";
import { TabNavigation, ActiveTab } from "@/components/layout/TabNavigation";
import { SituationRoom } from "@/components/modules/SituationRoom";
import { NetworkTopology } from "@/components/modules/NetworkTopology";
import { InventoryMonitoring } from "@/components/modules/InventoryMonitoring";
import { RiskMonitoring } from "@/components/modules/RiskMonitoring";
import { SimulationStudio } from "@/components/modules/SimulationStudio";
import { ScenarioComparison } from "@/components/modules/ScenarioComparison";
import { OptimizationRecommendations } from "@/components/modules/OptimizationRecommendations";
import { FinancialWaterfall } from "@/components/modules/FinancialWaterfall";
import { GovernanceInterface } from "@/components/modules/GovernanceInterface";
import BatchScenarioEngine from "@/components/modules/BatchScenarioEngine";
import DynamicPolicyOptimization from "@/components/modules/DynamicPolicyOptimization";
import DataIngestionCenter from "@/components/modules/DataIngestionCenter";

import {
  getSystemHealth,
  getDigitalTwinTopology,
  getInventorySummary,
  getActiveRisks,
  runSimulation,
  compareScenarios,
  solveOptimization,
  submitApproval,
  getAuditTrail,
} from "@/lib/api";

import {
  SystemHealth,
  DigitalTwinTopology,
  InventorySummaryResponse,
  ActiveRisk,
  SimulationRequest,
  SimulationResponse,
  ScenarioComparisonResponse,
  OptimizationRequest,
  OptimizationResult,
  ApprovalRequest,
  ApprovalResponse,
  AuditTrailResponse,
} from "@/lib/types";

export default function Home() {
  const [activeTab, setActiveTab] = useState<ActiveTab>("situation_room");

  // State from API
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [topology, setTopology] = useState<DigitalTwinTopology | null>(null);
  const [inventory, setInventory] = useState<InventorySummaryResponse | null>(null);
  const [risks, setRisks] = useState<ActiveRisk[]>([]);
  const [auditTrail, setAuditTrail] = useState<AuditTrailResponse | null>(null);

  // Simulation & Optimization State
  const [unmitigatedSim, setUnmitigatedSim] = useState<SimulationResponse | null>(null);
  const [mitigatedSim, setMitigatedSim] = useState<SimulationResponse | null>(null);
  const [comparisonResult, setComparisonResult] = useState<ScenarioComparisonResponse | null>(null);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);

  // Loading flags
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isSolving, setIsSolving] = useState(false);
  const [isApproving, setIsApproving] = useState(false);

  // Initial Data Fetch
  const loadInitialData = useCallback(async () => {
    setIsRefreshing(true);
    try {
      // 1. Fetch Health
      try {
        const h = await getSystemHealth();
        setHealth(h);
      } catch (err) {
        console.warn("Could not fetch health:", err);
      }

      // 2. Fetch Topology
      try {
        const top = await getDigitalTwinTopology();
        setTopology(top);
      } catch (err) {
        console.warn("Could not fetch topology:", err);
      }

      // 3. Fetch Inventory Summary
      try {
        const inv = await getInventorySummary();
        setInventory(inv);
      } catch (err) {
        console.warn("Could not fetch inventory:", err);
      }

      // 4. Fetch Active Risks
      try {
        const r = await getActiveRisks();
        setRisks(r.risks || []);
      } catch (err) {
        console.warn("Could not fetch risks:", err);
      }

      // 5. Fetch Audit Trail
      try {
        const aud = await getAuditTrail();
        setAuditTrail(aud);
      } catch (err) {
        console.warn("Could not fetch audit trail:", err);
      }

      // 6. Run Baseline Unmitigated Disruption Simulation
      const unmitReq: SimulationRequest = {
        scenario_name: "Status Quo Unmitigated Disruption",
        horizon_days: 90,
        shocks: {
          supplier_delays: [{ po_number: "PO-9012", delay_days: 21 }],
          freight_surcharges: [{ lane_id: "lane_east_coast_parcel", surcharge_percentage: 0.28 }],
          demand_elasticities: [{ sku_code: "APEX-JKT", demand_multiplier: 1.45, duration_days: 30 }],
        },
        mitigations: {},
      };

      // 7. Run Mitigated Optimal Plan Simulation
      const mitReq: SimulationRequest = {
        scenario_name: "ATLAS Optimal Mitigated Plan",
        horizon_days: 90,
        shocks: {
          supplier_delays: [{ po_number: "PO-9012", delay_days: 21 }],
          freight_surcharges: [{ lane_id: "lane_east_coast_parcel", surcharge_percentage: 0.28 }],
          demand_elasticities: [{ sku_code: "APEX-JKT", demand_multiplier: 1.45, duration_days: 30 }],
        },
        mitigations: {
          emergency_air_freight_units: 1500,
          inter_warehouse_transfer_units: 600,
          ad_spend_throttle_percentage: 0.18,
        },
      };

      try {
        const [uSim, mSim, comp] = await Promise.all([
          runSimulation(unmitReq),
          runSimulation(mitReq),
          compareScenarios(unmitReq, mitReq),
        ]);
        setUnmitigatedSim(uSim);
        setMitigatedSim(mSim);
        setComparisonResult(comp);
      } catch (err) {
        console.warn("Could not run initial simulations:", err);
      }
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const tabParam = params.get("tab") as ActiveTab;
      if (tabParam) {
        setActiveTab(tabParam);
      }
    }
    loadInitialData();
  }, [loadInitialData]);

  const handleTabChange = (tab: ActiveTab) => {
    setActiveTab(tab);
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("tab", tab);
      window.history.replaceState({}, "", url.toString());
    }
  };

  // Handler for custom simulation runs from Studio
  const handleRunSimulation = async (req: SimulationRequest): Promise<SimulationResponse> => {
    setIsSimulating(true);
    try {
      const resp = await runSimulation(req);
      setMitigatedSim(resp);
      return resp;
    } finally {
      setIsSimulating(false);
    }
  };

  // Handler for running Google OR-Tools optimization
  const handleSolveOptimization = async (req: OptimizationRequest): Promise<OptimizationResult> => {
    setIsSolving(true);
    try {
      const res = await solveOptimization(req);
      setOptimizationResult(res);

      // Also simulate with optimal decisions to update live scorecards
      const optimalSimReq: SimulationRequest = {
        scenario_name: "Google OR-Tools Optimal Solution",
        horizon_days: 90,
        shocks: {
          supplier_delays: [{ po_number: "PO-9012", delay_days: 21 }],
          freight_surcharges: [{ lane_id: "lane_east_coast_parcel", surcharge_percentage: 0.28 }],
          demand_elasticities: [{ sku_code: "APEX-JKT", demand_multiplier: 1.45, duration_days: 30 }],
        },
        mitigations: {
          emergency_air_freight_units: res.recommended_air_freight_units,
          inter_warehouse_transfer_units: res.recommended_transfer_units,
          ad_spend_throttle_percentage: res.recommended_ad_throttle_pct,
        },
      };
      const updatedSim = await runSimulation(optimalSimReq);
      setMitigatedSim(updatedSim);

      return res;
    } finally {
      setIsSolving(false);
    }
  };

  // Handler for submitting executive approval
  const handleSubmitApproval = async (req: ApprovalRequest): Promise<ApprovalResponse> => {
    setIsApproving(true);
    try {
      const resp = await submitApproval(req);
      return resp;
    } finally {
      setIsApproving(false);
    }
  };

  const handleRefreshAuditTrail = async () => {
    try {
      const aud = await getAuditTrail();
      setAuditTrail(aud);
    } catch (err) {
      console.warn("Error refreshing audit trail:", err);
    }
  };

  const criticalRisksCount = risks.filter((r) => r.severity === "CRITICAL").length;

  return (
    <div className="min-h-screen flex flex-col bg-command-950 text-slate-100">
      {/* Platform Header */}
      <Header health={health} onRefresh={loadInitialData} isRefreshing={isRefreshing} />

      {/* Main Tab Navigation */}
      <TabNavigation
        activeTab={activeTab}
        onTabChange={handleTabChange}
        criticalRiskCount={criticalRisksCount}
      />

      {/* Main Command Center Body */}
      <main className="flex-1 px-6 py-6 max-w-7xl mx-auto w-full">
        {/* Module 1: Situation Room */}
        {activeTab === "situation_room" && (
          <SituationRoom
            unmitigatedSim={unmitigatedSim}
            mitigatedSim={mitigatedSim}
            activeRisks={risks}
            onTriggerOptimization={() => {
              handleTabChange("optimization");
            }}
            onOpenSimulation={() => handleTabChange("simulation")}
            onOpenGovernance={() => handleTabChange("governance")}
          />
        )}

        {/* Module 2 & 3: Digital Twin & Inventory Monitoring */}
        {activeTab === "digital_twin" && (
          <div className="space-y-8">
            <NetworkTopology topology={topology} />
            <InventoryMonitoring inventory={inventory} />
          </div>
        )}

        {/* Module 4: Operational Risk Sentinels */}
        {activeTab === "risks" && (
          <RiskMonitoring
            risks={risks}
            onSimulateRisk={() => {
              handleTabChange("simulation");
            }}
          />
        )}

        {/* Module 5: Scenario Simulation Studio */}
        {activeTab === "simulation" && (
          <SimulationStudio
            onRunSimulation={handleRunSimulation}
            simulationResult={mitigatedSim || unmitigatedSim}
            isLoading={isSimulating}
          />
        )}

        {/* Module 6: Before-versus-After Scenario Comparison */}
        {activeTab === "comparison" && (
          <ScenarioComparison
            unmitigatedSim={unmitigatedSim}
            mitigatedSim={mitigatedSim}
            comparisonResult={comparisonResult}
          />
        )}

        {/* Module 7: Prescriptive Optimization Recommendations */}
        {activeTab === "optimization" && (
          <OptimizationRecommendations
            onSolveOptimization={handleSolveOptimization}
            optimizationResult={optimizationResult}
            onProceedToGovernance={(opt) => {
              handleTabChange("governance");
            }}
            isLoading={isSolving}
          />
        )}

        {/* Phase 3 Module A: Multi-Scenario Batch Engine & Sensitivity */}
        {activeTab === "batch" && (
          <BatchScenarioEngine />
        )}

        {/* Phase 3 Module B: Dynamic Policy Optimization & Sourcing */}
        {activeTab === "policy" && (
          <DynamicPolicyOptimization />
        )}

        {/* Phase 3 Module C: Enterprise Data Ingestion & Quality */}
        {activeTab === "ingestion" && (
          <DataIngestionCenter />
        )}

        {/* Module 8: Financial Impact & Contribution Margin Waterfall */}
        {activeTab === "waterfall" && (
          <FinancialWaterfall
            unmitigatedSim={unmitigatedSim}
            mitigatedSim={mitigatedSim}
          />
        )}

        {/* Module 9: Human Approval & Governance Interface */}
        {activeTab === "governance" && (
          <GovernanceInterface
            onSubmitApproval={handleSubmitApproval}
            auditTrail={auditTrail}
            onRefreshAuditTrail={handleRefreshAuditTrail}
            recommendedCapital={optimizationResult?.capital_required || 20670.0}
            isLoading={isApproving}
          />
        )}
      </main>

      {/* Platform Status Footer */}
      <footer className="border-t border-white/[0.06] bg-command-950 py-3 px-6 text-center text-xs text-slate-500 font-mono">
        SARAS ATLAS Enterprise Intelligence Platform • Zero-Cost Local Monolith • Target RAM &lt; 350 MB RSS • Vanguard Apparel Co. Benchmark
      </footer>
    </div>
  );
}
