"use client";

import React, { useState } from "react";
import {
  Compass,
  Network,
  AlertOctagon,
  TrendingDown,
  BarChart3,
  GitMerge,
  Zap,
  Target,
  ShieldCheck,
  FileText,
  ChevronLeft,
  ChevronRight,
  X,
  Play,
  CheckCircle2,
  ExternalLink,
  Info,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { ActiveTab } from "../layout/TabNavigation";

interface GuidedDemoModalProps {
  isOpen: boolean;
  onClose: () => void;
  activeTab: ActiveTab;
  onNavigateTab: (tab: ActiveTab) => void;
}

interface DemoStep {
  step: number;
  title: string;
  tab: ActiveTab;
  tabLabel: string;
  icon: React.ElementType;
  whatHappened: string;
  whyHappened: string;
  financialImpact: string;
  actionRequired: string;
  keyMetrics: { label: string; value: string; color?: string }[];
}

export function GuidedDemoModal({
  isOpen,
  onClose,
  activeTab,
  onNavigateTab,
}: GuidedDemoModalProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  if (!isOpen) return null;

  const demoSteps: DemoStep[] = [
    {
      step: 1,
      title: "1. Executive Situation Room & High-Level Posture",
      tab: "situation_room",
      tabLabel: "Situation Room",
      icon: Compass,
      whatHappened:
        "Vanguard Apparel Co. ($45M GMV synthetic benchmark) faces an active multi-echelon disruption triggered by shipment PO-9012 (10,000 units of Hero SKU APEX-JKT).",
      whyHappened:
        "Compound disruption cascade combining an upstream trans-Pacific maritime berth delay (+21 days), East Coast carrier spot surcharge (+28%), and viral TikTok influencer demand spike (+45%).",
      financialImpact:
        "$224,500.00 in gross commercial revenue exposure, projecting a -$129,844.32 GAAP net contribution margin erosion.",
      actionRequired:
        "Inspect early sentinel telemetry, review compound shock severity, and prepare prescriptive intervention.",
      keyMetrics: [
        { label: "Target SKU", value: "APEX-JKT (Apex Shell)" },
        { label: "Gross Revenue Exposed", value: "$224,500.00", color: "text-rose-400" },
        { label: "Net CM Erosion", value: "-$129,844.32", color: "text-rose-400" },
        { label: "Deficit Demand Units", value: "1,968 Units", color: "text-amber-400" },
      ],
    },
    {
      step: 2,
      title: "2. Inspect the Supply Chain Digital Twin",
      tab: "digital_twin",
      tabLabel: "Digital Twin & Inventory",
      icon: Network,
      whatHappened:
        "The digital twin tracks 3 primary distribution facilities (WH-WEST in Los Angeles/Reno, WH-CENTRAL in Dallas, WH-EAST in Allentown) and 4 global suppliers.",
      whyHappened:
        "Daily discrete conservation laws track inventory balances, safety stocks, inbound transit pipelines, and outbound customer fulfillment across the multi-echelon network.",
      financialImpact:
        "Stock depletion at Reno 3PL threatens high-margin West Coast direct-to-consumer fulfillment velocity.",
      actionRequired:
        "Verify facility capacities, safety stock levels (WH-EAST has 800 units reserve buffer), and transport lane costs.",
      keyMetrics: [
        { label: "Network Facilities", value: "3 Distribution Centers" },
        { label: "Global Suppliers", value: "4 Tier-1 Fabricators" },
        { label: "Allentown Safety Reserve", value: "800 Units Max" },
        { label: "Conservation Accuracy", value: "100.0% Exact" },
      ],
    },
    {
      step: 3,
      title: "3. Inject Shenzhen Supplier Disruption (PO-9012)",
      tab: "risks",
      tabLabel: "Risk Sentinels",
      icon: AlertOctagon,
      whatHappened:
        "Autonomous Risk Sentinel flags critical lead-time delay on PO-9012 from Pacific Garments Ltd (Shenzhen), delaying delivery from Day 18 to Day 39.",
      whyHappened:
        "Vessel congestion and terminal container dwell times at Shenzhen and Long Beach harbor extend lead times by 21 days.",
      financialImpact:
        "Imminent stockout warning: WH-WEST runout horizon reaches Day 34, causing a 10-day dead-zone before ocean replenishment arrives.",
      actionRequired:
        "Acknowledge the automated sentinel alert and initiate dynamic scenario simulation.",
      keyMetrics: [
        { label: "Vessel Dwell Delay", value: "+21 Days Berth Wait" },
        { label: "WH-WEST Runout", value: "Day 34 (Depletion)" },
        { label: "Sentinel Severity", value: "CRITICAL", color: "text-rose-400" },
        { label: "Status Quo Loss", value: "$224,500.00", color: "text-rose-400" },
      ],
    },
    {
      step: 4,
      title: "4. Observe Inventory & Demand Propagation",
      tab: "simulation",
      tabLabel: "Simulation Studio",
      icon: TrendingDown,
      whatHappened:
        "Daily discrete time-step simulation reveals that when WH-WEST runs dry on Day 34, demand spillover forces cross-country fulfillment from WH-EAST (Allentown) via Zone 8 parcel.",
      whyHappened:
        "Zone 8 cross-zone shipping costs spike to $21.50/unit (+28% freight surcharge), rapidly draining Allentown stock and causing secondary national stockouts.",
      financialImpact:
        "1,968 order units are completely lost to competitors; unit contribution margin collapses from $71.33 (39.6%) to $58.33 (32.4%).",
      actionRequired:
        "Evaluate simulated trajectory without intervention (Baseline Unmitigated Plan).",
      keyMetrics: [
        { label: "Cross-Zone Spillover", value: "24.8% of Total Orders" },
        { label: "Unfulfilled Demand", value: "1,968 Units" },
        { label: "Stockout Duration", value: "10 National Days" },
        { label: "Unit Margin Drop", value: "-$13.00 / Unit", color: "text-rose-400" },
      ],
    },
    {
      step: 5,
      title: "5. Inspect the Financial Impact Waterfall",
      tab: "waterfall",
      tabLabel: "Financial Waterfall",
      icon: BarChart3,
      whatHappened:
        "The GAAP Contribution Margin Waterfall rigorously separates Gross Commercial Revenue Exposure from Net Contribution Margin Erosion.",
      whyHappened:
        "Gross revenue exposed ($224,500.00 = 1,968 lost units × $180 retail + surcharges) overstates true economic damage because unfulfilled units do not incur factory FOB COGS and parcel shipping fees ($94,655.68 variable savings).",
      financialImpact:
        "Net contribution margin erosion is exactly $129,844.32 (at 57.84% net margin rate). Both figures are mathematically reconciled.",
      actionRequired:
        "Verify GAAP waterfall lines from gross retail price down to net contribution margin.",
      keyMetrics: [
        { label: "Gross Commercial Exposed", value: "$224,500.00", color: "text-amber-400" },
        { label: "Net CM Erosion (GAAP)", value: "$129,844.32", color: "text-rose-400" },
        { label: "Variable Cost Savings", value: "$94,655.68", color: "text-slate-400" },
        { label: "Baseline Unit CM", value: "$71.33 (39.63%)", color: "text-emerald-400" },
      ],
    },
    {
      step: 6,
      title: "6. Root Cause Analysis & Loss Decomposition",
      tab: "rca",
      tabLabel: "Root Cause Trace",
      icon: GitMerge,
      whatHappened:
        "Multi-tiered causal propagation traces the failure from Primary Trigger (PO-9012 maritime berth congestion) down into 5 discrete financial accounting loss segments.",
      whyHappened:
        "Decomposes loss across accounting buckets: Direct Inventory Shortage ($98,780 / 44.0%), Carrier Surcharges ($54,000 / 24.1%), SLA Penalties ($45,620 / 20.3%), Retail Cancellations ($18,100 / 8.1%), Rush Freight ($8,000 / 3.6%).",
      financialImpact:
        "Sum of 5 segments = exactly $224,500.00 (100.0% reconciled).",
      actionRequired:
        "Review partial sensitivity derivatives identifying lead-time variance as the #1 sensitivity driver (score: 0.92).",
      keyMetrics: [
        { label: "Primary Cause", value: "PO-9012 Maritime Berth Congestion" },
        { label: "Direct Shortage Loss", value: "$98,780.00 (44.0%)" },
        { label: "Carrier Surcharges", value: "$54,000.00 (24.1%)" },
        { label: "Reconciliation Parity", value: "100.0% Exact" },
      ],
    },
    {
      step: 7,
      title: "7. Run Mitigation Optimization (Google OR-Tools SCIP)",
      tab: "optimization",
      tabLabel: "Prescriptive MILP",
      icon: Zap,
      whatHappened:
        "The SCIP Mixed-Integer Linear Programming solver formulates an exact mathematical program under a $40,000.00 treasury working capital ceiling.",
      whyHappened:
        "Objective: Maximize Net Margin Contribution = 58.83·x_air + 81.13·x_xfer - 2500·ad_throttle subject to Budget (12.50·x_air + 3.20·x_xfer ≤ 40,000) and ground transfer safety ceiling (x_xfer ≤ 800).",
      financialImpact:
        "SCIP finds the provable global optimum in < 60 ms, prescribing an optimal capital deployment of $39,997.50 with $2.50 budget slack.",
      actionRequired:
        "Click 'Run Optimization' with $40,000 budget and observe the exact convergence.",
      keyMetrics: [
        { label: "Treasury Budget Ceiling", value: "$40,000.00" },
        { label: "Optimal Capital Outlay", value: "$39,997.50", color: "text-cyan-400" },
        { label: "Solver Convergence", value: "SCIP OPTIMAL", color: "text-emerald-400" },
        { label: "Budget Slack", value: "$2.50 (99.99% Deploy)" },
      ],
    },
    {
      step: 8,
      title: "8. Explain the Recommended Allocation",
      tab: "optimization",
      tabLabel: "Prescriptive MILP",
      icon: Target,
      whatHappened:
        "Why 800 ground units and 2,995 air units? Ground transfer provides superior efficiency ($25.35 profit / $ spent vs $4.71 / $ for air).",
      whyHappened:
        "Ground transfer is strictly constrained to 800 units by origin safety stock at Allentown DC. The solver maxes out all 800 ground units ($2,560.00), then greedily allocates all remaining $37,440.00 into 2,995 air units ($37,437.50).",
      financialImpact:
        "Restores fill rate to 99.8%, protects $129,844.32 in net contribution margin (3.25x ROI on spend), and generates a protective inventory buffer against future variance.",
      actionRequired:
        "Inspect the explainability rationale explaining the knapsack duality proof and safety stock limits.",
      keyMetrics: [
        { label: "Ground Units (Capped)", value: "800 Units ($2,560.00)" },
        { label: "Air Freight Units", value: "2,995 Units ($37,437.50)" },
        { label: "Ad Throttle", value: "0.0% (No dampening)" },
        { label: "Total Received Units", value: "3,795 Units (Full Cover)" },
      ],
    },
    {
      step: 9,
      title: "9. Demonstrate the Two-Man Rule Governance",
      tab: "governance",
      tabLabel: "Governance & Audit",
      icon: ShieldCheck,
      whatHappened:
        "Because the prescribed capital outlay ($39,997.50) exceeds the enterprise $25,000.00 policy threshold, the Two-Man Rule is automatically enforced.",
      whyHappened:
        "Enterprise controls prohibit unilateral capital disbursement above $25k. Dual authorization from both VP of Supply Chain (Marcus Vance) and Chief Financial Officer (Elena Rostova) is required.",
      financialImpact:
        "Prevents unvetted working capital drains while providing verifiable compliance for financial audit committees.",
      actionRequired:
        "Submit dual approvals and inspect the immutable SHA-256 cryptographic audit ledger.",
      keyMetrics: [
        { label: "Policy Threshold", value: "$25,000.00" },
        { label: "Mitigation Outlay", value: "$39,997.50 (> Threshold)", color: "text-amber-400" },
        { label: "Required Signoffs", value: "Dual (VP Ops + CFO)" },
        { label: "Audit Integrity", value: "SHA-256 Ledger Verified", color: "text-emerald-400" },
      ],
    },
    {
      step: 10,
      title: "10. Generate Executive PDF & CSV Reports",
      tab: "reports",
      tabLabel: "Executive Reports",
      icon: FileText,
      whatHappened:
        "Compile and export audit-ready board-level briefing dossier in both PDF and CSV formats.",
      whyHappened:
        "Both export formats share 100% data and structural parity, including identical headers, reconciled financial loss numbers ($224,500.00 gross vs $129,844.32 net), and governance signoff metadata.",
      financialImpact:
        "Provides the executive board with a defensible, mathematically verified decision audit trail.",
      actionRequired:
        "Download PDF and CSV briefings to complete the enterprise decision lifecycle.",
      keyMetrics: [
        { label: "PDF Report", value: "Audit-Ready (3 Pages)" },
        { label: "CSV Export", value: "Full Matrix (45 Rows)" },
        { label: "Data Parity", value: "100.0% Reconciled", color: "text-emerald-400" },
        { label: "Synthetic Disclaimer", value: "Vanguard ($45M GMV)" },
      ],
    },
  ];

  const currentStep = demoSteps[currentStepIndex];
  const StepIcon = currentStep.icon;

  const handleNext = () => {
    if (currentStepIndex < demoSteps.length - 1) {
      const nextIdx = currentStepIndex + 1;
      setCurrentStepIndex(nextIdx);
      onNavigateTab(demoSteps[nextIdx].tab);
    }
  };

  const handlePrevious = () => {
    if (currentStepIndex > 0) {
      const prevIdx = currentStepIndex - 1;
      setCurrentStepIndex(prevIdx);
      onNavigateTab(demoSteps[prevIdx].tab);
    }
  };

  const handleSelectStep = (index: number) => {
    setCurrentStepIndex(index);
    onNavigateTab(demoSteps[index].tab);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-command-950 border border-cyan-500/40 rounded-2xl shadow-[0_0_50px_rgba(6,182,212,0.3)] overflow-hidden my-6">
        {/* Synthetic Benchmark Warning Banner */}
        <div className="bg-amber-950/70 border-b border-amber-500/30 px-6 py-2 text-xs text-amber-200 flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <span className="font-bold uppercase tracking-wider text-amber-400 bg-amber-900/80 px-1.5 py-0.5 rounded text-[10px] border border-amber-500/40">
              SYNTHETIC EXECUTIVE DEMO
            </span>
            <span>
              All data represents synthetic benchmark data for Vanguard Apparel Co. ($45M GMV). No real customer data is used.
            </span>
          </div>
          <span className="font-mono text-[11px] text-amber-400/80">Step {currentStep.step} of 10</span>
        </div>

        {/* Modal Header */}
        <div className="bg-gradient-to-r from-cyan-950/80 via-command-900 to-command-950 p-5 border-b border-white/[0.08] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 shadow-[0_0_15px_rgba(6,182,212,0.3)]">
              <StepIcon className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400">
                  EXECUTIVE WALKTHROUGH TOUR
                </span>
                <Badge variant="cyan" size="sm">
                  {currentStep.tabLabel}
                </Badge>
              </div>
              <h3 className="text-lg font-bold text-white mt-0.5">{currentStep.title}</h3>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-lg bg-white/[0.04] hover:bg-white/[0.08] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-6 max-h-[68vh] overflow-y-auto">
          {/* Step Progress Indicators */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-white/[0.06] no-scrollbar">
            {demoSteps.map((s, idx) => (
              <button
                key={s.step}
                onClick={() => handleSelectStep(idx)}
                className={`px-2.5 py-1 rounded text-[11px] font-mono shrink-0 transition-all ${
                  idx === currentStepIndex
                    ? "bg-cyan-500 text-black font-bold shadow-[0_0_10px_rgba(6,182,212,0.4)]"
                    : idx < currentStepIndex
                    ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/40"
                    : "bg-command-900 text-slate-400 hover:text-white"
                }`}
              >
                {idx < currentStepIndex ? "✓" : ""} Step {s.step}
              </button>
            ))}
          </div>

          {/* 4 Decision Dimensions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
            <div className="p-4 rounded-xl bg-command-900 border border-white/[0.06]">
              <span className="font-mono text-[10px] uppercase font-bold text-cyan-400 block mb-1">
                1. What Happened?
              </span>
              <p className="text-slate-200 leading-relaxed">{currentStep.whatHappened}</p>
            </div>

            <div className="p-4 rounded-xl bg-command-900 border border-white/[0.06]">
              <span className="font-mono text-[10px] uppercase font-bold text-indigo-400 block mb-1">
                2. Why Did It Happen?
              </span>
              <p className="text-slate-200 leading-relaxed">{currentStep.whyHappened}</p>
            </div>

            <div className="p-4 rounded-xl bg-command-900 border border-white/[0.06]">
              <span className="font-mono text-[10px] uppercase font-bold text-rose-400 block mb-1">
                3. Financial Impact &amp; Exposure
              </span>
              <p className="text-slate-200 leading-relaxed">{currentStep.financialImpact}</p>
            </div>

            <div className="p-4 rounded-xl bg-command-900 border border-white/[0.06]">
              <span className="font-mono text-[10px] uppercase font-bold text-emerald-400 block mb-1">
                4. Prescribed Decision Action
              </span>
              <p className="text-slate-200 leading-relaxed">{currentStep.actionRequired}</p>
            </div>
          </div>

          {/* Key Metrics Strip */}
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold block mb-2">
              Verified Step Evidence Metrics
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
              {currentStep.keyMetrics.map((km, i) => (
                <div
                  key={i}
                  className="p-3 rounded-lg bg-command-900/90 border border-white/[0.06] text-center"
                >
                  <span className="text-[10px] text-slate-400 block truncate">{km.label}</span>
                  <span
                    className={`text-sm font-bold block mt-0.5 ${
                      km.color || "text-white"
                    }`}
                  >
                    {km.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal Footer Controls */}
        <div className="bg-command-900/80 p-4 border-t border-white/[0.08] flex items-center justify-between flex-wrap gap-3">
          <button
            onClick={() => onNavigateTab(currentStep.tab)}
            className="text-xs font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1.5 transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Currently Viewing: {currentStep.tabLabel}</span>
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrevious}
              disabled={currentStepIndex === 0}
              className="px-3.5 py-2 rounded-lg bg-command-800 hover:bg-command-750 border border-white/[0.08] text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentStepIndex < demoSteps.length - 1 ? (
              <button
                onClick={handleNext}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider shadow-[0_0_15px_rgba(6,182,212,0.4)] flex items-center gap-1.5 transition-transform hover:scale-[1.02]"
              >
                <span>Next Step</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={onClose}
                className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold uppercase tracking-wider shadow-[0_0_15px_rgba(16,185,129,0.4)] flex items-center gap-1.5 transition-colors"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Finish Demonstration</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
