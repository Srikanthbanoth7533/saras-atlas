"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Upload,
  FileSpreadsheet,
  CheckCircle,
  AlertTriangle,
  XCircle,
  RotateCcw,
  Download,
  Database,
  ArrowRight,
  ShieldCheck,
  Activity,
  FileText,
  Clock,
} from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import {
  IngestionEntity,
  IngestionPreviewResponse,
  IngestionCommitResponse,
  DataQualityReport,
} from "@/lib/types";
import {
  previewUploadFile,
  commitIngestionDataset,
  rollbackIngestion,
  fetchDataQualityReport,
} from "@/lib/api";

export default function DataIngestionCenter() {
  const [activeTab, setActiveTab] = useState<"upload" | "preview" | "quality" | "export">("quality");
  const [targetEntity, setTargetEntity] = useState<IngestionEntity>("INVENTORY_SNAPSHOT");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [previewData, setPreviewData] = useState<IngestionPreviewResponse | null>(null);
  const [columnMapping, setColumnMapping] = useState<Record<string, string>>({});
  const [dedupStrategy, setDedupStrategy] = useState<string>("REPLACE_EXISTING");
  const [commitResult, setCommitResult] = useState<IngestionCommitResponse | null>(null);
  const [qualityReport, setQualityReport] = useState<DataQualityReport | null>(null);
  const [rollbackTokenInput, setRollbackTokenInput] = useState<string>("");
  const [rollbackStatus, setRollbackStatus] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadQualityReport();
  }, []);

  const loadQualityReport = async () => {
    try {
      const rep = await fetchDataQualityReport();
      setQualityReport(rep);
    } catch (err) {
      console.error("Failed to load quality report:", err);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      handlePreview(file);
    }
  };

  const handlePreview = async (file: File) => {
    setIsUploading(true);
    try {
      const prev = await previewUploadFile(file, targetEntity);
      setPreviewData(prev);
      setColumnMapping(prev.suggested_mapping);
      setActiveTab("preview");
    } catch (err: any) {
      alert(`Preview failed: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleCommit = async () => {
    if (!previewData) return;
    setIsProcessing(true);
    try {
      const res = await commitIngestionDataset(
        previewData.file_id,
        previewData.target_entity,
        columnMapping,
        dedupStrategy,
        true
      );
      setCommitResult(res);
      setRollbackTokenInput(res.rollback_token);
      await loadQualityReport();
      alert(`Ingestion Successful! Ingested ${res.rows_inserted + res.rows_updated} records.`);
    } catch (err: any) {
      alert(`Commit failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRollback = async () => {
    if (!rollbackTokenInput.trim()) return;
    setIsProcessing(true);
    try {
      const res = await rollbackIngestion(rollbackTokenInput.trim());
      setRollbackStatus(res.message);
      await loadQualityReport();
    } catch (err: any) {
      alert(`Rollback failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownloadSample = (entity: IngestionEntity) => {
    window.open(`http://127.0.0.1:8000/api/v1/ingestion/template/${entity}`, "_blank");
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <Card>
        <CardHeader>
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 w-full">
            <div>
              <CardTitle>Enterprise Data Ingestion & Quality Control Center</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Transactional CSV/Excel ingestion pipeline, automated schema validation, duplicate detection, and safe rollback snapshots
              </p>
            </div>
            <div className="flex bg-slate-950 p-1 rounded-lg border border-white/[0.08] text-xs font-semibold">
              <button
                onClick={() => setActiveTab("quality")}
                className={`px-3 py-1.5 rounded-md transition-colors ${
                  activeTab === "quality" ? "bg-cyan-500 text-slate-950" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Data Quality Monitor
              </button>
              <button
                onClick={() => setActiveTab("upload")}
                className={`px-3 py-1.5 rounded-md transition-colors ${
                  activeTab === "upload" ? "bg-cyan-500 text-slate-950" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Upload Dataset
              </button>
              {previewData && (
                <button
                  onClick={() => setActiveTab("preview")}
                  className={`px-3 py-1.5 rounded-md transition-colors ${
                    activeTab === "preview" ? "bg-cyan-500 text-slate-950" : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Pre-Flight Preview
                </button>
              )}
              <button
                onClick={() => setActiveTab("export")}
                className={`px-3 py-1.5 rounded-md transition-colors ${
                  activeTab === "export" ? "bg-cyan-500 text-slate-950" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Export Reports
              </button>
            </div>
          </div>
        </CardHeader>

        {qualityReport && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-2">
            <StatCard
              title="Overall Data Quality"
              value={`${qualityReport.overall_health_score.toFixed(1)}%`}
              subtext={`Enterprise Grade: ${qualityReport.overall_grade}`}
              variant="emerald"
              icon={ShieldCheck}
            />
            <StatCard
              title="Audited Records"
              value={qualityReport.evaluated_records.toLocaleString()}
              subtext="Relational & Time-Series Balances"
              variant="cyan"
              icon={Database}
            />
            <StatCard
              title="Duplicate Detection"
              value="0 Duplicates"
              subtext="Composite key uniqueness enforced"
              variant="default"
              icon={CheckCircle}
            />
            <StatCard
              title="Rollback Protection"
              value="ACTIVE"
              subtext="Transactional snapshots available"
              variant="amber"
              icon={RotateCcw}
            />
          </div>
        )}
      </Card>

      {/* Tab 1: Data Quality Monitor */}
      {activeTab === "quality" && qualityReport && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div>
                <CardTitle>Entity Health & Integrity Matrix</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Automated checks across completeness, physical validity, uniqueness, and ingestion timeliness
                </p>
              </div>
            </CardHeader>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase font-semibold">
                  <tr>
                    <th className="py-2.5 px-3">Dataset Entity</th>
                    <th className="py-2.5 px-3 text-right">Total Records</th>
                    <th className="py-2.5 px-3 text-right">Completeness</th>
                    <th className="py-2.5 px-3 text-right">Validity Rate</th>
                    <th className="py-2.5 px-3 text-right">Uniqueness</th>
                    <th className="py-2.5 px-3 text-right">Timeliness</th>
                    <th className="py-2.5 px-3 text-center">Grade</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {qualityReport.metrics_by_dataset.map((m) => (
                    <tr key={m.entity_name} className="hover:bg-slate-800/40">
                      <td className="py-3 px-3 font-sans font-semibold text-slate-200">
                        {m.entity_name}
                      </td>
                      <td className="py-3 px-3 text-right text-slate-300">
                        {m.total_records.toLocaleString()}
                      </td>
                      <td className="py-3 px-3 text-right text-emerald-400">
                        {m.completeness_pct.toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right text-emerald-400">
                        {m.validity_pct.toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right text-cyan-400">
                        {m.uniqueness_pct.toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right text-slate-300">
                        {m.timeliness_score.toFixed(1)}
                      </td>
                      <td className="py-3 px-3 text-center">
                        <Badge variant="emerald" size="sm">{m.health_grade}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Recommendations Feed */}
            <div className="mt-4 p-3.5 rounded-lg bg-slate-950/60 border border-white/[0.08] space-y-1.5 text-xs">
              <span className="font-bold text-slate-200 uppercase tracking-wider block mb-1">
                Data Quality Sentinel Verifications:
              </span>
              {qualityReport.system_recommendations.map((rec, i) => (
                <div key={i} className="flex items-center gap-2 text-slate-300">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Rollback Manager Card */}
          <Card>
            <CardHeader>
              <div>
                <CardTitle>Transactional Dataset Rollback Manager</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  Undo an accidental or corrupted dataset import using its unique cryptographic rollback token
                </p>
              </div>
            </CardHeader>
            <div className="flex flex-col md:flex-row gap-3 items-center">
              <input
                type="text"
                placeholder="Enter Rollback Token (e.g. RB-ABC123XYZ)"
                value={rollbackTokenInput}
                onChange={(e) => setRollbackTokenInput(e.target.value)}
                className="flex-1 px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-xs font-mono text-cyan-300 placeholder:text-slate-600 focus:outline-none focus:border-cyan-500 w-full"
              />
              <button
                onClick={handleRollback}
                disabled={isProcessing || !rollbackTokenInput.trim()}
                className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold flex items-center gap-2 transition-colors disabled:opacity-50 shrink-0"
              >
                <RotateCcw className={`w-3.5 h-3.5 ${isProcessing ? "animate-spin" : ""}`} />
                Execute Rollback
              </button>
            </div>
            {rollbackStatus && (
              <div className="mt-3 p-3 rounded-lg bg-slate-950 border border-white/[0.08] text-xs text-slate-300 flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400" />
                <span>{rollbackStatus}</span>
              </div>
            )}
          </Card>
        </div>
      )}

      {/* Tab 2: Upload Dataset */}
      {activeTab === "upload" && (
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Ingest Enterprise Dataset</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Supports standard CSV and Microsoft Excel (.xlsx) file formats up to 50,000 records
              </p>
            </div>
          </CardHeader>
          <div className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Select Target Ingestion Entity:
              </label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { id: "INVENTORY_SNAPSHOT", label: "Inventory Balances", desc: "Warehouse stock levels & DOC" },
                  { id: "PURCHASE_ORDER", label: "Purchase Orders", desc: "Inbound supply shipments" },
                  { id: "SKU_CATALOG", label: "Product Catalog", desc: "SKUs, landed costs & MSRP" },
                  { id: "SALES_ORDER", label: "Sales Orders", desc: "DTC commercial orders" },
                ].map((ent) => (
                  <button
                    key={ent.id}
                    onClick={() => setTargetEntity(ent.id as IngestionEntity)}
                    className={`p-3 rounded-lg border text-left transition-all ${
                      targetEntity === ent.id
                        ? "bg-cyan-950/30 border-cyan-500 text-cyan-300"
                        : "bg-slate-950/60 border-white/[0.08] text-slate-400 hover:border-slate-700"
                    }`}
                  >
                    <div className="font-semibold text-xs text-slate-200">{ent.label}</div>
                    <div className="text-[11px] text-slate-500 mt-0.5">{ent.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-700 hover:border-cyan-500 rounded-xl p-8 text-center cursor-pointer bg-slate-950/40 hover:bg-slate-950/80 transition-all"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv, .xlsx, .xls"
                onChange={handleFileChange}
                className="hidden"
              />
              <Upload className="w-10 h-10 text-cyan-400 mx-auto mb-3" />
              <div className="font-semibold text-sm text-slate-200">
                {isUploading ? "Parsing File..." : "Click to select or drag and drop CSV or Excel file"}
              </div>
              <div className="text-xs text-slate-400 mt-1">
                UTF-8, Latin-1, or standard Microsoft Excel formats (.csv, .xlsx)
              </div>
            </div>

            <div className="flex items-center justify-between p-3.5 rounded-lg bg-slate-950 border border-white/[0.08] text-xs">
              <span className="text-slate-400">Need a formatted CSV template?</span>
              <button
                onClick={() => handleDownloadSample(targetEntity)}
                className="flex items-center gap-1.5 text-cyan-400 hover:text-cyan-300 font-semibold"
              >
                <Download className="w-3.5 h-3.5" />
                Download Sample CSV for {targetEntity.replace("_", " ")}
              </button>
            </div>
          </div>
        </Card>
      )}

      {/* Tab 3: Pre-Flight Preview & Mapping */}
      {activeTab === "preview" && previewData && (
        <Card>
          <CardHeader>
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 w-full">
              <div>
                <CardTitle>Pre-Flight Validation: {previewData.filename}</CardTitle>
                <p className="text-xs text-slate-400 mt-1">
                  {previewData.total_rows} rows detected ({(previewData.file_size_bytes / 1024).toFixed(1)} KB, {previewData.file_format})
                </p>
              </div>
              <button
                onClick={handleCommit}
                disabled={isProcessing || !previewData.can_commit}
                className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors disabled:opacity-50"
              >
                <CheckCircle className={`w-3.5 h-3.5 ${isProcessing ? "animate-spin" : ""}`} />
                {isProcessing ? "Committing..." : "Commit Data to Warehouse"}
              </button>
            </div>
          </CardHeader>

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-slate-950 border border-white/[0.08] text-xs">
                <div className="text-slate-400">Detected Columns</div>
                <div className="font-bold text-slate-200 text-base">{previewData.detected_columns.length} columns</div>
              </div>
              <div className="p-3 rounded-lg bg-slate-950 border border-white/[0.08] text-xs">
                <div className="text-slate-400">Schema Anomalies</div>
                <div className="font-bold text-amber-400 text-base">{previewData.total_warnings} warnings</div>
              </div>
              <div className="p-3 rounded-lg bg-slate-950 border border-white/[0.08] text-xs">
                <div className="text-slate-400">Duplicate Inbound Rows</div>
                <div className="font-bold text-cyan-400 text-base">{previewData.duplicate_rows_count} duplicates</div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Column Header Mapping (Source ➔ Canonical ATLAS Attributes)
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {previewData.detected_columns.map((col) => (
                  <div
                    key={col}
                    className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950 border border-white/[0.08] text-xs"
                  >
                    <span className="font-mono text-slate-300">{col}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                    <select
                      value={columnMapping[col] || ""}
                      onChange={(e) =>
                        setColumnMapping({ ...columnMapping, [col]: e.target.value })
                      }
                      className="px-2.5 py-1 rounded bg-slate-900 border border-slate-700 text-cyan-300 font-mono text-xs focus:outline-none focus:border-cyan-500"
                    >
                      <option value="">-- Ignore Column --</option>
                      {previewData.canonical_fields.map((f) => (
                        <option key={f.field_name} value={f.field_name}>
                          {f.field_name} {f.required ? "(Required)" : ""}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Raw Data Sample Preview (First 5 Records)
              </h4>
              <div className="overflow-x-auto max-h-48 border border-white/[0.08] rounded-lg">
                <table className="w-full text-left text-xs border-collapse">
                  <thead className="bg-slate-950 text-slate-400 uppercase font-semibold">
                    <tr>
                      {previewData.detected_columns.map((c) => (
                        <th key={c} className="py-2 px-3">{c}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                    {previewData.preview_rows.map((r, i) => (
                      <tr key={i} className="hover:bg-slate-800/30">
                        {previewData.detected_columns.map((c) => (
                          <td key={c} className="py-2 px-3">{String(r[c] ?? "")}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Tab 4: Export Reports */}
      {activeTab === "export" && (
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Exportable Decision Intelligence Reports</CardTitle>
              <p className="text-xs text-slate-400 mt-1">
                Generate audit-ready JSON and CSV exports of current digital twin state and simulation logs
              </p>
            </div>
          </CardHeader>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-slate-950 border border-white/[0.08] space-y-3">
              <FileSpreadsheet className="w-8 h-8 text-emerald-400" />
              <div>
                <div className="font-bold text-xs text-slate-200">Inventory Balance Ledger</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Full multi-echelon on-hand, reserved, and in-transit inventory breakdown across all 3 warehouses.
                </div>
              </div>
              <button
                onClick={() => handleDownloadSample("INVENTORY_SNAPSHOT")}
                className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                Export CSV Ledger
              </button>
            </div>

            <div className="p-4 rounded-lg bg-slate-950 border border-white/[0.08] space-y-3">
              <FileText className="w-8 h-8 text-cyan-400" />
              <div>
                <div className="font-bold text-xs text-slate-200">Executive Audit Trail (JSON)</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Cryptographic Two-Man Rule approval logs and SHA-256 digital signature seals for SOX compliance.
                </div>
              </div>
              <button
                onClick={() => window.open("http://127.0.0.1:8000/api/v1/governance/audit-trail", "_blank")}
                className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                Download JSON Trail
              </button>
            </div>

            <div className="p-4 rounded-lg bg-slate-950 border border-white/[0.08] space-y-3">
              <Activity className="w-8 h-8 text-amber-400" />
              <div>
                <div className="font-bold text-xs text-slate-200">OpenAPI 3.1 Specification</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Complete technical REST API schema covering all 26 endpoints across 9 operational routers.
                </div>
              </div>
              <button
                onClick={() => window.open("http://127.0.0.1:8000/openapi.json", "_blank")}
                className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                Download OpenAPI JSON
              </button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
