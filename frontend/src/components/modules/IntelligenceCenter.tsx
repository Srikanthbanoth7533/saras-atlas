"use client";

import React, { useState, useEffect } from "react";
import {
  BrainCircuit,
  Search,
  Sparkles,
  ShieldCheck,
  Database,
  ArrowRight,
  ExternalLink,
  Layers,
  CheckCircle2,
  AlertCircle,
  Clock,
} from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { askIntelligence, fetchSampleQueries } from "@/lib/api";
import { IntelligenceResponse, GroundedCitation } from "@/lib/types";

export default function IntelligenceCenter() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [sampleQueries, setSampleQueries] = useState<string[]>([]);
  const [response, setResponse] = useState<IntelligenceResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSampleQueries()
      .then(setSampleQueries)
      .catch(() => {
        setSampleQueries([
          "What is our stockout risk and days of coverage across warehouses?",
          "How is the PO-9012 Shenzhen delay impacting our GAAP contribution margin?",
          "What actions does the OR-Tools solver recommend to protect EBITDA?",
        ]);
      });
    // Run an initial default grounded query
    handleQuery("What is our stockout risk and days of coverage across warehouses?");
  }, []);

  const handleQuery = async (queryText: string) => {
    if (!queryText.trim()) return;
    setLoading(true);
    setError(null);
    setQuery(queryText);
    try {
      const data = await askIntelligence(queryText);
      setResponse(data);
    } catch (err: any) {
      setError(err?.message || "Failed to process decision intelligence query.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-950/60 via-slate-900 to-slate-900 border border-blue-800/40 rounded-xl p-6 shadow-xl relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="p-2 bg-blue-500/20 text-blue-400 rounded-lg">
                <BrainCircuit className="w-6 h-6" />
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                AI Decision Intelligence & Grounded Business Analysis
              </h2>
              <Badge variant="emerald" className="text-xs">
                100% Deterministic Grounding
              </Badge>
            </div>
            <p className="text-sm text-slate-300 max-w-3xl">
              Ask natural-language questions across inventory, supplier reliability, demand surges,
              and contribution margins. Every metric is mathematically verified and cited directly
              from the live digital twin state — zero LLM token costs, zero hallucinations.
            </p>
          </div>
          <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-800/70 px-3 py-2 rounded-lg border border-slate-700/60 shrink-0">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Audit-Ready Citations</span>
          </div>
        </div>
      </div>

      {/* Query Bar */}
      <Card className="p-4 bg-slate-900/90 border-slate-800 shadow-md">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleQuery(query);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask Atlas e.g., 'What is our stockout risk by warehouse?' or 'Explain PO-9012 margin impact'..."
              className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-11 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white font-medium text-sm rounded-lg transition-colors flex items-center justify-center space-x-2 shrink-0 shadow-lg shadow-blue-900/30"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Grounding Data...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Analyze & Ground</span>
              </>
            )}
          </button>
        </form>

        {/* Sample query pills */}
        {sampleQueries.length > 0 && (
          <div className="mt-3.5 pt-3 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
            <span className="text-xs text-slate-400 font-medium">Quick Inquiries:</span>
            {sampleQueries.map((sq, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleQuery(sq)}
                className="text-xs bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-white px-2.5 py-1 rounded-md transition-colors border border-slate-700/50"
              >
                {sq}
              </button>
            ))}
          </div>
        )}
      </Card>

      {/* Error Banner */}
      {error && (
        <div className="p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 flex items-center space-x-3 text-sm">
          <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Grounded Answer Area */}
      {response && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Structured Answer & Telemetry */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Domain Intent:
                  </span>
                  <Badge variant="cyan">{response.intent_topic}</Badge>
                </div>
                <div className="flex items-center space-x-4 text-xs text-slate-400">
                  <div className="flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>Confidence: {(response.confidence_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex items-center space-x-1.5">
                    <Database className="w-4 h-4 text-blue-400" />
                    <span className="font-mono text-slate-300">{response.data_freshness}</span>
                  </div>
                </div>
              </div>

              {/* Render Markdown Text */}
              <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-3 whitespace-pre-line font-sans">
                {response.answer_markdown}
              </div>

              {/* Proactive Action Triggers */}
              {response.suggested_actions.length > 0 && (
                <div className="mt-6 pt-5 border-t border-slate-800">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
                    <ArrowRight className="w-4 h-4 text-blue-400" />
                    <span>Recommended Proactive Interventions</span>
                  </h4>
                  <ul className="space-y-2">
                    {response.suggested_actions.map((act, i) => (
                      <li
                        key={i}
                        className="text-xs text-slate-300 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 flex items-start space-x-2"
                      >
                        <span className="text-blue-400 font-bold shrink-0">{i + 1}.</span>
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </Card>
          </div>

          {/* Right Col: Grounded Fact Citations Ledger */}
          <div className="space-y-6">
            <Card className="p-5 bg-slate-900/90 border-slate-800">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Verified Grounding Citations</span>
                </CardTitle>
              </CardHeader>
              <p className="text-xs text-slate-400 mb-4">
                Every business metric is directly cited from verified relational tables in the
                underlying SQLite WAL store.
              </p>

              {response.citations.length === 0 ? (
                <p className="text-xs text-slate-500 italic">No direct entity citations required.</p>
              ) : (
                <div className="space-y-3">
                  {response.citations.map((c, i) => (
                    <div
                      key={i}
                      className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1.5"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-mono text-blue-400 font-semibold">{c.source_entity}</span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {c.record_key}
                        </span>
                      </div>
                      <div className="text-xs text-slate-300">
                        <span className="text-slate-400">{c.metric_name}: </span>
                        <span className="font-semibold text-emerald-300">{c.verified_value}</span>
                      </div>
                      <div className="text-[10px] text-slate-500 flex items-center space-x-1">
                        <Clock className="w-3 h-3 text-slate-600" />
                        <span>Verified: {new Date(c.audit_timestamp).toLocaleTimeString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            {/* Grounded Key Metrics Card */}
            {Object.keys(response.grounded_metrics).length > 0 && (
              <Card className="p-5 bg-slate-900/90 border-slate-800">
                <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                  <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                    <Database className="w-4 h-4 text-blue-400" />
                    <span>Telemetry Metrics</span>
                  </CardTitle>
                </CardHeader>
                <div className="space-y-2 text-xs">
                  {Object.entries(response.grounded_metrics).map(([k, v], idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-2 bg-slate-950/50 rounded border border-slate-800/60"
                    >
                      <span className="text-slate-400 font-mono text-[11px]">{k}</span>
                      <span className="text-slate-200 font-semibold font-mono text-[11px]">
                        {typeof v === "object" ? JSON.stringify(v) : String(v)}
                      </span>
                    </div>
                  ))}
                </div>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
