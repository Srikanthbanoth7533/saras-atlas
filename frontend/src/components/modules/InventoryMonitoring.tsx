"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { InventorySummaryResponse, SkuInventoryItem } from "@/lib/types";
import { Warehouse, Ship, Clock, AlertCircle, CheckCircle2, Search, Filter } from "lucide-react";
import { formatCurrency, formatNumber } from "@/lib/utils";

interface InventoryMonitoringProps {
  inventory: InventorySummaryResponse | null;
}

export function InventoryMonitoring({ inventory }: InventoryMonitoringProps) {
  const [search, setSearch] = useState("");
  const items = inventory?.items || [];

  const filteredItems = items.filter(
    (item) =>
      item.sku_code?.toLowerCase().includes(search.toLowerCase()) ||
      (item.product_name || item.product_title || "")
        .toLowerCase()
        .includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* 1. Warehouse Nodes Status & Days of Coverage (DOC) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Reno 3PL */}
        <div className="command-panel rounded-xl p-4 border border-rose-500/40 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-16 w-16 bg-rose-500/10 rounded-bl-full pointer-events-none" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              WH-WEST-RENO (3PL)
            </span>
            <Badge variant="rose" size="sm">
              DEPLETING FAST
            </Badge>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono text-white">1,150 Units</span>
            <span className="text-xs font-mono text-rose-400 font-bold">DOC: 8.2 Days</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Fulfills West Coast (50% demand). Enters stockout on Day 9 without emergency air/transfer.
          </p>
          <div className="mt-3 h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-rose-500 w-[24%]" />
          </div>
        </div>

        {/* Allentown 3PL */}
        <div className="command-panel rounded-xl p-4 border border-amber-500/40 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-16 w-16 bg-amber-500/10 rounded-bl-full pointer-events-none" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              WH-EAST-ALLENTOWN (3PL)
            </span>
            <Badge variant="amber" size="sm">
              ELEVATED STRAIN
            </Badge>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono text-white">2,100 Units</span>
            <span className="text-xs font-mono text-amber-400 font-bold">DOC: 18.5 Days</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Fulfills East Coast (40% demand). Impacted by +28% parcel surcharge; potential cross-zone drain.
          </p>
          <div className="mt-3 h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-amber-500 w-[58%]" />
          </div>
        </div>

        {/* Dallas Central Hub */}
        <div className="command-panel rounded-xl p-4 border border-emerald-500/40 relative overflow-hidden">
          <div className="absolute top-0 right-0 h-16 w-16 bg-emerald-500/10 rounded-bl-full pointer-events-none" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              WH-CENTRAL-DALLAS
            </span>
            <Badge variant="emerald" size="sm">
              HEALTHY BUFFER
            </Badge>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono text-white">450 Units</span>
            <span className="text-xs font-mono text-emerald-400 font-bold">DOC: 22.5 Days</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Fulfills Central US (10% demand). Secondary fallback node with stable ground transit lanes.
          </p>
          <div className="mt-3 h-2 w-full bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-emerald-500 w-[72%]" />
          </div>
        </div>
      </div>

      {/* 2. Inbound Purchase Order Pipeline Monitor */}
      <Card className="command-panel border-white/[0.08]">
        <CardHeader>
          <div className="flex items-center gap-2.5">
            <Ship className="w-5 h-5 text-cyan-400" />
            <CardTitle>Inbound Maritime & Air Pipeline Status</CardTitle>
          </div>
          <Badge variant="outline" size="sm">
            4 PURCHASE ORDERS MONITORED
          </Badge>
        </CardHeader>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-command-900/80 text-slate-400 font-mono uppercase tracking-wider border-b border-white/[0.06]">
              <tr>
                <th className="py-2.5 px-3">PO Number</th>
                <th className="py-2.5 px-3">SKU / Item</th>
                <th className="py-2.5 px-3">Quantity</th>
                <th className="py-2.5 px-3">Vessel / Carrier</th>
                <th className="py-2.5 px-3">Destination</th>
                <th className="py-2.5 px-3">Original ETA</th>
                <th className="py-2.5 px-3">Current ETA</th>
                <th className="py-2.5 px-3">Pipeline Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04] font-mono">
              <tr className="bg-rose-950/20 hover:bg-rose-950/30 transition-colors">
                <td className="py-2.5 px-3 font-bold text-rose-400">PO-9012</td>
                <td className="py-2.5 px-3 text-white">Apex Shell Jacket (Hero SKU)</td>
                <td className="py-2.5 px-3 font-bold text-white">10,000 units</td>
                <td className="py-2.5 px-3 text-slate-300">Ever Forward (Ocean)</td>
                <td className="py-2.5 px-3 text-slate-300">Reno, NV</td>
                <td className="py-2.5 px-3 text-slate-400 line-through">Day 6</td>
                <td className="py-2.5 px-3 font-bold text-rose-400">Day 27 (+21d)</td>
                <td className="py-2.5 px-3">
                  <Badge variant="rose" size="sm">
                    PORT BOTTLENECK
                  </Badge>
                </td>
              </tr>
              <tr className="hover:bg-white/[0.02] transition-colors">
                <td className="py-2.5 px-3 font-bold text-slate-200">PO-9014</td>
                <td className="py-2.5 px-3 text-slate-300">Apex Technical Shell (All sizes)</td>
                <td className="py-2.5 px-3 text-white">4,000 units</td>
                <td className="py-2.5 px-3 text-slate-300">Cosco Glory (Ocean)</td>
                <td className="py-2.5 px-3 text-slate-300">Dallas, TX</td>
                <td className="py-2.5 px-3 text-slate-400">Day 28</td>
                <td className="py-2.5 px-3 text-emerald-400">Day 28 (On Time)</td>
                <td className="py-2.5 px-3">
                  <Badge variant="emerald" size="sm">
                    IN TRANSIT
                  </Badge>
                </td>
              </tr>
              <tr className="hover:bg-white/[0.02] transition-colors">
                <td className="py-2.5 px-3 font-bold text-slate-200">PO-9016</td>
                <td className="py-2.5 px-3 text-slate-300">Technical Fleece Line</td>
                <td className="py-2.5 px-3 text-white">5,000 units</td>
                <td className="py-2.5 px-3 text-slate-300">Maersk Mc-Kinney (Ocean)</td>
                <td className="py-2.5 px-3 text-slate-300">Allentown, PA</td>
                <td className="py-2.5 px-3 text-slate-400">Day 48</td>
                <td className="py-2.5 px-3 text-emerald-400">Day 48 (On Time)</td>
                <td className="py-2.5 px-3">
                  <Badge variant="emerald" size="sm">
                    SCHEDULED
                  </Badge>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      {/* 3. SKU Catalog Inventory Balances */}
      <Card className="command-panel border-white/[0.08]">
        <CardHeader>
          <div className="flex items-center justify-between w-full flex-wrap gap-3">
            <div className="flex items-center gap-2.5">
              <Warehouse className="w-5 h-5 text-indigo-400" />
              <CardTitle>Catalog Inventory Positions ({items.length} SKUs Monitored)</CardTitle>
            </div>
            <div className="relative w-64">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search SKU or product..."
                className="w-full bg-command-900 border border-white/[0.08] rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50"
              />
            </div>
          </div>
        </CardHeader>

        <div className="overflow-x-auto max-h-96 overflow-y-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-command-900/80 text-slate-400 uppercase tracking-wider sticky top-0 border-b border-white/[0.06]">
              <tr>
                <th className="py-2 px-3">SKU Code</th>
                <th className="py-2 px-3">Product Name</th>
                <th className="py-2 px-3">Retail Price</th>
                <th className="py-2 px-3">On-Hand</th>
                <th className="py-2 px-3">Available</th>
                <th className="py-2 px-3">Min DOC</th>
                <th className="py-2 px-3">Stock Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04]">
              {filteredItems.slice(0, 15).map((sku) => {
                const isCritical = sku.status === "CRITICAL_STOCKOUT";
                const isAtRisk = sku.status === "AT_RISK";

                return (
                  <tr key={sku.sku_id} className="hover:bg-white/[0.02] transition-colors">
                    <td className="py-2 px-3 font-bold text-cyan-400">{sku.sku_code}</td>
                    <td className="py-2 px-3 text-slate-200">{sku.product_name || sku.product_title || "Apex Technical Garment"}</td>
                    <td className="py-2 px-3 text-slate-300">{formatCurrency(sku.retail_price)}</td>
                    <td className="py-2 px-3 text-white font-bold">{formatNumber(sku.total_on_hand)}</td>
                    <td className="py-2 px-3 text-slate-300">{formatNumber(sku.total_available)}</td>
                    <td className="py-2 px-3">
                      <span className={isCritical ? "text-rose-400 font-bold" : isAtRisk ? "text-amber-400" : "text-emerald-400"}>
                        {sku.min_days_of_coverage.toFixed(1)}d
                      </span>
                    </td>
                    <td className="py-2 px-3">
                      <Badge
                        variant={isCritical ? "rose" : isAtRisk ? "amber" : "emerald"}
                        size="sm"
                      >
                        {sku.status}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

