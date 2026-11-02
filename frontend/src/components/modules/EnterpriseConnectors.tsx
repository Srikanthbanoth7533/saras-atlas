"use client";

import React, { useState, useEffect } from "react";
import {
  Database,
  Cloud,
  CheckCircle2,
  AlertCircle,
  Play,
  Table,
  Lock,
  Layers,
  Search,
  ExternalLink,
  ShieldCheck,
  Server,
  Terminal,
} from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { fetchConnectors, testConnector, discoverConnectorSchema } from "@/lib/api";
import { ConnectorConfig, ConnectionTestResult, SchemaDiscoveryResponse } from "@/lib/types";

export default function EnterpriseConnectors() {
  const [connectors, setConnectors] = useState<ConnectorConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<Record<string, ConnectionTestResult>>({});
  const [selectedSchema, setSelectedSchema] = useState<SchemaDiscoveryResponse | null>(null);
  const [schemaLoading, setSchemaLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchConnectors()
      .then(setConnectors)
      .catch((err) => setError(err?.message || "Failed to load connectors."))
      .finally(() => setLoading(false));
  }, []);

  const handleTestConnection = async (id: string) => {
    setTestingId(id);
    try {
      const res = await testConnector(id);
      setTestResults((prev) => ({ ...prev, [id]: res }));
    } catch (err: any) {
      alert(`Test connection failed: ${err?.message}`);
    } finally {
      setTestingId(null);
    }
  };

  const handleDiscoverSchema = async (id: string) => {
    setSchemaLoading(true);
    try {
      const res = await discoverConnectorSchema(id);
      setSelectedSchema(res);
    } catch (err: any) {
      alert(`Schema discovery failed: ${err?.message}`);
    } finally {
      setSchemaLoading(false);
    }
  };

  const getConnectorBadge = (type: string) => {
    switch (type) {
      case "BIGQUERY":
        return <Badge variant="cyan">Google Cloud</Badge>;
      case "SNOWFLAKE":
        return <Badge variant="cyan">Snowflake</Badge>;
      case "AMAZON_REDSHIFT":
        return <Badge variant="amber">AWS Cloud</Badge>;
      case "REST_WEBHOOK":
        return <Badge variant="default">Webhooks</Badge>;
      default:
        return <Badge variant="emerald">Local File System</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-teal-950/40 to-slate-900 border border-teal-800/40 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="p-2 bg-teal-500/20 text-teal-400 rounded-lg">
                <Cloud className="w-6 h-6" />
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                Enterprise Cloud Warehouse & API Connectors
              </h2>
              <Badge variant="emerald" className="text-xs">
                Zero-Cost Sandbox Mode
              </Badge>
            </div>
            <p className="text-sm text-slate-300 max-w-3xl">
              Prepared integration architecture for Google BigQuery, Snowflake, Amazon Redshift,
              REST Webhooks, and CSV/Excel. All live syncs remain optional and run in dry-run
              sandbox mode without requiring paid subscriptions or external credentials.
            </p>
          </div>
          <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-800/70 px-3 py-2 rounded-lg border border-slate-700/60 shrink-0">
            <Lock className="w-4 h-4 text-emerald-400" />
            <span>Zero-Credential Leak Confirmed</span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <span>Discovering enterprise connector catalog...</span>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm">
          {error}
        </div>
      )}

      {!loading && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Connector Cards List */}
          <div className="lg:col-span-2 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Registered Enterprise Connectors ({connectors.length})
            </h3>

            {connectors.map((c) => {
              const test = testResults[c.connector_id];
              return (
                <Card
                  key={c.connector_id}
                  className="p-5 bg-slate-900/90 border-slate-800 hover:border-slate-700 transition-colors"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-2">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-slate-950 border border-slate-800 rounded-lg">
                        <Database className="w-5 h-5 text-teal-400" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="text-sm font-bold text-white">{c.name}</h4>
                          {getConnectorBadge(c.connector_type)}
                        </div>
                        <span className="text-xs text-slate-500 font-mono">
                          ID: {c.connector_id} | Host: {c.host || "Local Process"}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleTestConnection(c.connector_id)}
                        disabled={testingId === c.connector_id}
                        className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center space-x-1.5 transition-colors"
                      >
                        {testingId === c.connector_id ? (
                          <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                          <Play className="w-3.5 h-3.5 text-teal-400" />
                        )}
                        <span>Test Ping</span>
                      </button>

                      <button
                        onClick={() => handleDiscoverSchema(c.connector_id)}
                        className="px-3 py-1.5 bg-slate-950 hover:bg-slate-800 text-slate-300 text-xs font-semibold rounded-lg border border-slate-800 flex items-center space-x-1.5 transition-colors"
                      >
                        <Table className="w-3.5 h-3.5 text-blue-400" />
                        <span>Schema</span>
                      </button>
                    </div>
                  </div>

                  <p className="text-xs text-slate-400 mb-3">{c.description}</p>

                  {/* Test Ping Result Banner */}
                  {test && (
                    <div className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs flex items-start justify-between gap-2">
                      <div className="flex items-start space-x-2">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-semibold text-emerald-300">{test.status}: </span>
                          <span className="text-slate-300">{test.message}</span>
                          <div className="text-[10px] text-slate-500 font-mono mt-0.5">
                            Discovered: {test.discovered_tables.join(", ")} | Latency:{" "}
                            {test.latency_ms} ms
                          </div>
                        </div>
                      </div>
                      <Badge variant="emerald" className="text-[10px] shrink-0 font-mono">
                        {test.latency_ms} ms
                      </Badge>
                    </div>
                  )}
                </Card>
              );
            })}
          </div>

          {/* Schema Viewer Panel */}
          <div>
            <Card className="p-5 bg-slate-900/90 border-slate-800 sticky top-6">
              <CardHeader className="p-0 pb-3 mb-3 border-b border-slate-800">
                <CardTitle className="text-sm font-bold text-white flex items-center space-x-2">
                  <Table className="w-4 h-4 text-blue-400" />
                  <span>Schema Catalog Introspection</span>
                </CardTitle>
              </CardHeader>

              {schemaLoading && (
                <div className="p-8 text-center text-slate-400 text-xs">
                  <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                  <span>Introspecting schema catalog...</span>
                </div>
              )}

              {!selectedSchema && !schemaLoading && (
                <p className="text-xs text-slate-500 italic p-4 text-center">
                  Select "Schema" on any connector to view table definitions and column types.
                </p>
              )}

              {selectedSchema && !schemaLoading && (
                <div className="space-y-4">
                  <div className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Dialect:</span>
                      <span className="font-mono text-teal-300 font-semibold">
                        {selectedSchema.dialect}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Database/Dataset:</span>
                      <span className="font-mono text-slate-200">
                        {selectedSchema.database}.{selectedSchema.schema_name}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Sync Mode:</span>
                      <span className="font-mono text-slate-200">
                        {selectedSchema.recommended_sync_mode}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {Object.entries(selectedSchema.tables).map(([tableName, cols]) => (
                      <div
                        key={tableName}
                        className="p-3 bg-slate-950/60 rounded-lg border border-slate-800/80"
                      >
                        <span className="font-mono font-bold text-xs text-blue-400 block mb-2">
                          {tableName} ({cols.length} cols)
                        </span>
                        <div className="space-y-1 text-[11px] font-mono">
                          {cols.map((col, idx) => (
                            <div key={idx} className="flex justify-between text-slate-400">
                              <span>{col.column}</span>
                              <span className="text-slate-500">{col.type}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}
