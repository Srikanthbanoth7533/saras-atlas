"use client";

import React, { useState, useEffect } from "react";
import {
  FileText,
  Download,
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  Printer,
  ShieldCheck,
  Building,
  Calendar,
  Layers,
  ArrowRight,
} from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { fetchExecutiveReportSummary, API_BASE } from "@/lib/api";
import { ExecutiveReportData } from "@/lib/types";

export default function ExecutiveReportingCenter() {
  const [report, setReport] = useState<ExecutiveReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchExecutiveReportSummary()
      .then(setReport)
      .catch((err) => setError(err?.message || "Failed to load executive report summary."))
      .finally(() => setLoading(false));
  }, []);

  const handleDownloadPdf = () => {
    window.open(`${API_BASE}/reports/export/pdf`, "_blank");
  };

  const handleDownloadCsv = () => {
    window.open(`${API_BASE}/reports/export/csv`, "_blank");
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-sky-950/40 to-slate-900 border border-sky-800/40 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="p-2 bg-sky-500/20 text-sky-400 rounded-lg">
                <FileText className="w-6 h-6" />
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                Executive Reporting & Board Decision Center
              </h2>
              <Badge variant="cyan" className="text-xs">
                Export Ready (PDF / CSV)
              </Badge>
            </div>
            <p className="text-sm text-slate-300 max-w-3xl">
              Generate and download audit-ready executive briefings summarizing live business digital
              twin posture, active supply chain disruptions, root cause decomposition, and prescriptive
              mitigation decisions.
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={handleDownloadPdf}
              className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold rounded-lg flex items-center space-x-2 transition-colors shadow-lg shadow-sky-900/30"
            >
              <Download className="w-4 h-4" />
              <span>Download PDF</span>
            </button>
            <button
              onClick={handleDownloadCsv}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center space-x-2 transition-colors"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span>Download CSV</span>
            </button>
          </div>
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-sky-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <span>Compiling executive report dossier...</span>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm">
          {error}
        </div>
      )}

      {report && (
        <div className="space-y-6">
          {/* Executive Summary Card */}
          <Card className="p-6 bg-slate-900/90 border-slate-800 shadow-md">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-800 gap-2">
              <div>
                <span className="text-xs uppercase font-mono tracking-wider text-sky-400 font-bold block">
                  Executive Briefing Dossier
                </span>
                <h3 className="text-base font-bold text-white">{report.title}</h3>
                <span className="text-xs text-slate-400">{report.enterprise}</span>
              </div>
              <div className="text-right text-xs text-slate-400 flex items-center space-x-1.5">
                <Calendar className="w-3.5 h-3.5 text-slate-500" />
                <span>Generated: {report.generated_at}</span>
              </div>
            </div>

            <p className="text-sm text-slate-200 leading-relaxed font-sans bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 mb-6">
              {report.executive_summary}
            </p>

            {/* Strategic KPI Table */}
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              Strategic KPI Posture: Baseline vs Unmitigated vs ATLAS Mitigated
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-mono">
                    {report.kpi_posture[0]?.map((header, i) => (
                      <th key={i} className="pb-2.5">
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {report.kpi_posture.slice(1).map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/30">
                      <td className="py-2.5 font-sans font-medium text-white">{row[0]}</td>
                      <td className="py-2.5 text-slate-400">{row[1]}</td>
                      <td className="py-2.5 text-rose-400">{row[2]}</td>
                      <td className="py-2.5 text-sky-300 font-bold">{row[3]}</td>
                      <td className="py-2.5 text-emerald-400 font-bold">{row[4]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          {/* Two-Column Detail: RCA & Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left: Root Cause Analysis */}
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                  <span>Root Cause Analysis & Loss Decomposition</span>
                </CardTitle>
              </CardHeader>
              <div className="mb-4">
                <span className="text-xs text-slate-400 font-bold block mb-1">Primary Root Cause:</span>
                <span className="text-xs font-semibold text-rose-300 bg-rose-950/40 px-2.5 py-1 rounded border border-rose-800/50 block">
                  {report.root_cause_analysis.primary_cause}
                </span>
              </div>
              <p className="text-xs text-slate-300 mb-4 leading-relaxed">
                {report.root_cause_analysis.narrative}
              </p>

              <div className="space-y-2 text-xs">
                {report.root_cause_analysis.attributions.map((attr, idx) => (
                  <div
                    key={idx}
                    className="p-2.5 bg-slate-950/70 rounded-lg border border-slate-800/80 flex items-center justify-between"
                  >
                    <span className="text-slate-300 font-medium">{attr[0]}</span>
                    <span className="font-mono font-bold text-rose-400">
                      {attr[1]} ({attr[2]})
                    </span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Right: Prescriptive Recommendations */}
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Prescriptive Optimization Decisions</span>
                </CardTitle>
              </CardHeader>

              <div className="space-y-3">
                {report.recommendations.map((rec) => (
                  <div
                    key={rec.rank}
                    className="p-3 bg-slate-950/70 rounded-lg border border-slate-800/90 space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-white">
                        #{rec.rank} — {rec.title}
                      </span>
                      <span className="font-mono text-emerald-400 font-bold text-[11px]">
                        {rec.financial_benefit.split(" ")[0]} Lift
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300">{rec.action}</p>
                    <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-slate-800/60">
                      <span>Capital: {rec.capital}</span>
                      <span className="text-amber-400">Inaction: {rec.consequences_inaction.slice(0, 45)}...</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Governance Box & Disclaimers */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="p-5 bg-slate-900/90 border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Governance Sign-Off Posture</span>
              </h4>
              <div className="text-xs space-y-1.5 text-slate-300">
                <p>
                  <span className="text-slate-500 font-medium">Mandate:</span>{" "}
                  {report.governance.mandate}
                </p>
                <p>
                  <span className="text-slate-500 font-medium">Operations:</span>{" "}
                  {report.governance.approver_1}
                </p>
                <p>
                  <span className="text-slate-500 font-medium">Finance:</span>{" "}
                  {report.governance.approver_2}
                </p>
              </div>
            </Card>

            <Card className="p-5 bg-slate-900/90 border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                Assumptions & Safeguards
              </h4>
              <ul className="text-[11px] text-slate-400 space-y-1">
                {report.assumptions_and_limitations.slice(0, 3).map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}
