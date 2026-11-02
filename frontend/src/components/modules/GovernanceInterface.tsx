"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ApprovalRequest, ApprovalResponse, AuditTrailResponse } from "@/lib/types";
import { ShieldCheck, ShieldAlert, Key, CheckCircle2, History, AlertCircle, FileText, Lock } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

interface GovernanceInterfaceProps {
  onSubmitApproval: (req: ApprovalRequest) => Promise<ApprovalResponse>;
  auditTrail: AuditTrailResponse | null;
  onRefreshAuditTrail: () => void;
  recommendedCapital?: number;
  isLoading?: boolean;
}

export function GovernanceInterface({
  onSubmitApproval,
  auditTrail,
  onRefreshAuditTrail,
  recommendedCapital = 20670.0,
  isLoading = false,
}: GovernanceInterfaceProps) {
  // Two-Man Rule State
  const [primaryId, setPrimaryId] = useState("USR-COO-01");
  const [primaryName, setPrimaryName] = useState("Elena Rostova (Chief Operating Officer)");
  const [secondaryId, setSecondaryId] = useState("USR-CFO-01");
  const [secondaryName, setSecondaryName] = useState("Marcus Vance (Chief Financial Officer)");
  const [capitalOutlay, setCapitalOutlay] = useState(recommendedCapital);
  const [decision, setDecision] = useState<"APPROVED" | "REJECTED" | "MODIFIED">("APPROVED");
  const [notes, setNotes] = useState(
    "Authorized emergency air freight (1,500 units Saigon) and inter-node transfer (600 units Allentown->Reno) to bridge PO-9012 berthing delay."
  );

  const [validationError, setValidationError] = useState<string | null>(null);
  const [latestApproval, setLatestApproval] = useState<ApprovalResponse | null>(null);

  useEffect(() => {
    setCapitalOutlay(recommendedCapital);
  }, [recommendedCapital]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    if (primaryId.trim().toLowerCase() === secondaryId.trim().toLowerCase()) {
      setValidationError("Two-Man Rule Violation: Primary and Secondary executive approvers must be distinct individuals.");
      return;
    }

    try {
      const resp = await onSubmitApproval({
        approver_primary_id: primaryId,
        approver_primary_name: primaryName,
        approver_secondary_id: secondaryId,
        approver_secondary_name: secondaryName,
        decision: decision,
        notes: notes,
        approved_capital_outlay: Number(capitalOutlay),
      });
      setLatestApproval(resp);
      onRefreshAuditTrail();
    } catch (err: any) {
      setValidationError(err.message || "Failed to commit approval record.");
    }
  };

  return (
    <div className="space-y-6">
      {/* 1. Governance Sandbox Security Disclaimer */}
      <div className="command-panel rounded-xl p-4 border border-indigo-500/30 bg-gradient-to-r from-indigo-950/50 via-command-900/80 to-command-950 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-indigo-950 text-indigo-400 border border-indigo-800/60 shadow-[0_0_12px_rgba(99,102,241,0.3)]">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold text-indigo-400 uppercase tracking-wider">
                ENTERPRISE DECISION GOVERNANCE
              </span>
              <Badge variant="purple" size="sm">TWO-MAN RULE ENFORCED</Badge>
              <Badge variant="outline" size="sm">SANDBOX BOUNDARY</Badge>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              Simulated Decision Authority: Approval records compute cryptographic SHA-256 digital seals for verifiable auditability. Real-world financial disbursements are decoupled from this decision simulation engine.
            </p>
          </div>
        </div>
      </div>

      {/* 2. Interactive Two-Man Rule Sign-off Form */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="command-panel border-white/[0.08]">
          <CardHeader>
            <div className="flex items-center gap-2.5">
              <Key className="w-5 h-5 text-cyan-400" />
              <CardTitle>Dual-Key Executive Sign-Off (Two-Man Rule)</CardTitle>
            </div>
            <Badge variant="cyan" size="sm">DUAL AUTHORIZATION</Badge>
          </CardHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            {validationError && (
              <div className="p-3 rounded-lg bg-rose-950/70 border border-rose-800/60 text-xs text-rose-300 flex items-center gap-2 font-mono">
                <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                <span>{validationError}</span>
              </div>
            )}

            {/* Primary Approver */}
            <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
              <span className="text-xs font-mono uppercase text-slate-400 block mb-1">
                Primary Approver (Operations / Supply Chain)
              </span>
              <div className="grid grid-cols-3 gap-2">
                <input
                  type="text"
                  value={primaryId}
                  onChange={(e) => setPrimaryId(e.target.value)}
                  placeholder="Approver ID"
                  className="bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-cyan-400 focus:outline-none focus:border-cyan-500"
                />
                <input
                  type="text"
                  value={primaryName}
                  onChange={(e) => setPrimaryName(e.target.value)}
                  placeholder="Full Name & Role"
                  className="col-span-2 bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
            </div>

            {/* Secondary Approver */}
            <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
              <span className="text-xs font-mono uppercase text-slate-400 block mb-1">
                Secondary Approver (Finance / Treasury)
              </span>
              <div className="grid grid-cols-3 gap-2">
                <input
                  type="text"
                  value={secondaryId}
                  onChange={(e) => setSecondaryId(e.target.value)}
                  placeholder="Approver ID"
                  className="bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-indigo-400 focus:outline-none focus:border-indigo-500"
                />
                <input
                  type="text"
                  value={secondaryName}
                  onChange={(e) => setSecondaryName(e.target.value)}
                  placeholder="Full Name & Role"
                  className="col-span-2 bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-white focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            {/* Capital & Decision */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
                <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
                  Committed Capital Outlay ($)
                </label>
                <input
                  type="number"
                  value={capitalOutlay}
                  onChange={(e) => setCapitalOutlay(Number(e.target.value))}
                  className="w-full bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-white font-bold focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
                <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
                  Executive Decision
                </label>
                <select
                  value={decision}
                  onChange={(e) => setDecision(e.target.value as any)}
                  className="w-full bg-command-950 border border-white/[0.1] rounded px-2 py-1.5 font-mono text-xs text-emerald-400 font-bold focus:outline-none focus:border-cyan-500"
                >
                  <option value="APPROVED">APPROVED (AUTHORIZE)</option>
                  <option value="MODIFIED">MODIFIED (CONDITIONAL)</option>
                  <option value="REJECTED">REJECTED (ABORT)</option>
                </select>
              </div>
            </div>

            {/* Executive Notes */}
            <div className="bg-command-900 border border-white/[0.06] rounded-lg p-3">
              <label className="text-xs font-mono uppercase text-slate-400 block mb-1">
                Justification & Audit Notes
              </label>
              <textarea
                rows={2}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full bg-command-950 border border-white/[0.1] rounded px-2.5 py-1.5 font-mono text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2.5 rounded-lg bg-gradient-to-r from-emerald-500 to-cyan-600 hover:from-emerald-400 hover:to-cyan-500 text-white text-xs font-bold uppercase tracking-wider flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(16,185,129,0.3)] transition-all disabled:opacity-50"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>{isLoading ? "Signing Audit Payload..." : "Execute Dual-Signature Authorization"}</span>
            </button>
          </form>
        </Card>

        {/* Latest Digital Signature Seal Output */}
        <div className="space-y-4">
          <Card className="command-panel border-cyan-500/30">
            <CardHeader>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <CardTitle>Active Cryptographic Approval Seal</CardTitle>
              </div>
              <Badge variant="emerald" size="sm">
                {latestApproval ? latestApproval.status : "READY FOR SIGN-OFF"}
              </Badge>
            </CardHeader>

            {latestApproval ? (
              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 rounded-lg bg-command-950/80 border border-white/[0.06]">
                  <span className="text-slate-400 text-[10px] uppercase block">SHA-256 Digital Signature</span>
                  <span className="text-cyan-400 font-bold break-all">{latestApproval.digital_signature_sha256}</span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="p-2 rounded bg-command-900 border border-white/[0.04]">
                    <span className="text-slate-400 block">Primary Signer</span>
                    <span className="text-white font-semibold">{latestApproval.approver_primary}</span>
                  </div>
                  <div className="p-2 rounded bg-command-900 border border-white/[0.04]">
                    <span className="text-slate-400 block">Secondary Signer</span>
                    <span className="text-white font-semibold">{latestApproval.approver_secondary}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-[11px] pt-1">
                  <span className="text-slate-400">Committed Capital:</span>
                  <span className="font-bold text-emerald-400">{formatCurrency(latestApproval.approved_capital_outlay)}</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-slate-400">Timestamp (UTC):</span>
                  <span className="text-slate-300">{latestApproval.created_at}</span>
                </div>
              </div>
            ) : (
              <div className="p-6 text-center text-xs text-slate-400 font-mono">
                Submit dual executive credentials to generate an immutable SHA-256 digital signature seal.
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* 3. Immutable Governance Audit Trail History */}
      <Card className="command-panel border-white/[0.08]">
        <CardHeader>
          <div className="flex items-center gap-2.5">
            <History className="w-5 h-5 text-indigo-400" />
            <CardTitle>Immutable Governance & Decision Audit Trail</CardTitle>
          </div>
          <Badge variant="outline" size="sm">
            {auditTrail?.total_approvals_recorded || 0} AUDITED COMMITMENTS
          </Badge>
        </CardHeader>

        <div className="overflow-x-auto max-h-72 overflow-y-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-command-900/80 text-slate-400 uppercase tracking-wider sticky top-0 border-b border-white/[0.06]">
              <tr>
                <th className="py-2.5 px-3">Approval ID</th>
                <th className="py-2.5 px-3">Approver Signatures</th>
                <th className="py-2.5 px-3">Decision</th>
                <th className="py-2.5 px-3">SHA-256 Hash</th>
                <th className="py-2.5 px-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04]">
              {(auditTrail?.recent_approvals || []).map((appr) => (
                <tr key={appr.id} className="hover:bg-white/[0.02]">
                  <td className="py-2 px-3 text-cyan-400 font-bold">{appr.id.slice(0, 8)}...</td>
                  <td className="py-2 px-3 text-white">{appr.approver}</td>
                  <td className="py-2 px-3">
                    <Badge variant={appr.decision === "APPROVED" ? "emerald" : "rose"} size="sm">
                      {appr.decision}
                    </Badge>
                  </td>
                  <td className="py-2 px-3 text-slate-400 font-mono text-[11px] truncate max-w-xs">
                    {appr.digital_signature_hash}
                  </td>
                  <td className="py-2 px-3 text-slate-400 text-[11px]">
                    {appr.created_at ? new Date(appr.created_at).toLocaleString() : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
