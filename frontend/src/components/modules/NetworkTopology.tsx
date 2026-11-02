"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { DigitalTwinTopology, TopologyNode, TopologyEdge } from "@/lib/types";
import { Network, Warehouse, Factory, Ship, Plane, Truck, CheckCircle2, AlertTriangle, Layers } from "lucide-react";

interface NetworkTopologyProps {
  topology: DigitalTwinTopology | null;
}

export function NetworkTopology({ topology }: NetworkTopologyProps) {
  const [selectedNode, setSelectedNode] = useState<TopologyNode | null>(null);

  // Nodes defined with visual positions for clear schematic layout
  const visualNodes = [
    {
      id: "supp_shenzhen_01",
      name: "Shenzhen Apparel Factory",
      code: "FAC-SHENZHEN",
      type: "SUPPLIER",
      x: 120,
      y: 120,
      country: "China",
      status: "DELAYED_INBOUND",
      statusText: "PO-9012 Berthing Bottleneck (+21d)",
      onHand: "10,000 units on vessel",
    },
    {
      id: "supp_vietnam_02",
      name: "Saigon Garments Co.",
      code: "FAC-SAIGON",
      type: "SUPPLIER",
      x: 120,
      y: 280,
      country: "Vietnam",
      status: "AIR_BACKUP",
      statusText: "Air Expediting Ready (8d lead time)",
      onHand: "3,000 units capacity",
    },
    {
      id: "wh_west_reno",
      name: "West Coast 3PL (Reno)",
      code: "WH-WEST-RENO",
      type: "WAREHOUSE",
      x: 520,
      y: 130,
      region: "Western US (50% Demand)",
      status: "CRITICAL_STOCKOUT_RISK",
      statusText: "Stocks Out Day 9 Without Mitigation",
      onHand: "1,150 units on-hand",
    },
    {
      id: "wh_central_dallas",
      name: "Central Distribution Hub (Dallas)",
      code: "WH-CENTRAL-DALLAS",
      type: "WAREHOUSE",
      x: 640,
      y: 280,
      region: "Central US (10% Demand)",
      status: "NORMAL",
      statusText: "Healthy Buffer",
      onHand: "450 units on-hand",
    },
    {
      id: "wh_east_allentown",
      name: "East Coast 3PL (Allentown)",
      code: "WH-EAST-ALLENTOWN",
      type: "WAREHOUSE",
      x: 820,
      y: 140,
      region: "Eastern US (40% Demand)",
      status: "CROSS_ZONE_DRAIN",
      statusText: "Carrier Surcharge +28% • X-Zone Risk",
      onHand: "2,100 units on-hand",
    },
  ];

  return (
    <div className="space-y-6">
      <Card className="command-panel border-white/[0.08]">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-950/80 border border-cyan-800/60 text-cyan-400">
              <Network className="w-5 h-5" />
            </div>
            <div>
              <CardTitle>Business Digital Twin — Multi-Echelon Network Topology</CardTitle>
              <p className="text-xs text-slate-400 mt-0.5">
                Real-time schematic of overseas factories, trans-pacific maritime corridors, and domestic 3PL nodes
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="rose" size="sm">
              <Ship className="w-3 h-3" /> PO-9012 Delayed +21d
            </Badge>
            <Badge variant="cyan" size="sm">
              <Truck className="w-3 h-3" /> Allentown → Reno Transfer Ready
            </Badge>
          </div>
        </CardHeader>

        {/* Interactive SVG Network Diagram */}
        <div className="relative bg-command-950/90 rounded-xl border border-white/[0.06] p-4 overflow-hidden">
          <svg viewBox="0 0 960 400" className="w-full h-auto max-h-[460px]">
            <defs>
              <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#EF4444" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#EF4444" stopOpacity="0.2" />
              </linearGradient>
              <linearGradient id="airGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#06B6D4" stopOpacity="0.9" />
                <stop offset="100%" stopColor="#6366F1" stopOpacity="0.9" />
              </linearGradient>
              <linearGradient id="transferGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#10B981" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#06B6D4" stopOpacity="0.8" />
              </linearGradient>

              {/* Marker heads */}
              <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#EF4444" />
              </marker>
              <marker id="arrow-cyan" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#06B6D4" />
              </marker>
              <marker id="arrow-emerald" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981" />
              </marker>
            </defs>

            {/* Edge 1: Trans-Pacific Maritime Delay (Shenzhen to Reno) */}
            <path
              d="M 170 120 C 320 80, 420 100, 520 130"
              fill="none"
              stroke="url(#oceanGrad)"
              strokeWidth="3"
              strokeDasharray="6,6"
              markerEnd="url(#arrow-red)"
              className="animate-pulse"
            />
            <text x="320" y="85" fill="#EF4444" fontSize="11" fontFamily="monospace" fontWeight="bold">
              [OCEAN] PO-9012 (10,000 units) • DELAYED +21 DAYS
            </text>

            {/* Edge 2: Emergency Air Freight (Saigon to Reno) */}
            <path
              d="M 170 280 C 330 290, 430 200, 520 145"
              fill="none"
              stroke="url(#airGrad)"
              strokeWidth="2.5"
              strokeDasharray="4,4"
              markerEnd="url(#arrow-cyan)"
            />
            <text x="280" y="240" fill="#06B6D4" fontSize="11" fontFamily="monospace" fontWeight="bold">
              [AIR EXPEDITED] Saigon Backup (1,500 units @ $12.50)
            </text>

            {/* Edge 3: Inter-Warehouse Ground Transfer (Allentown to Reno) */}
            <path
              d="M 820 155 C 720 220, 620 180, 535 140"
              fill="none"
              stroke="url(#transferGrad)"
              strokeWidth="2.5"
              markerEnd="url(#arrow-emerald)"
            />
            <text x="640" y="210" fill="#10B981" fontSize="11" fontFamily="monospace" fontWeight="bold">
              [GROUND LTL] Transfer (600 units @ $3.20)
            </text>

            {/* Domestic Hub Connections */}
            <line x1="530" y1="145" x2="635" y2="275" stroke="#334155" strokeWidth="1.5" strokeDasharray="3,3" />
            <line x1="645" y1="275" x2="815" y2="150" stroke="#334155" strokeWidth="1.5" strokeDasharray="3,3" />

            {/* Node Renderings */}
            {visualNodes.map((n) => {
              const isSelected = selectedNode?.id === n.id;
              const isSupplier = n.type === "SUPPLIER";
              const isCritical = n.status === "CRITICAL_STOCKOUT_RISK" || n.status === "DELAYED_INBOUND";

              return (
                <g
                  key={n.id}
                  transform={`translate(${n.x}, ${n.y})`}
                  onClick={() => setSelectedNode(n as any)}
                  className="cursor-pointer group"
                >
                  <circle
                    r={isSelected ? "26" : "22"}
                    fill={isSupplier ? "#1E1B4B" : isCritical ? "#450A0A" : "#0F172A"}
                    stroke={isSelected ? "#06B6D4" : isCritical ? "#EF4444" : "#3B82F6"}
                    strokeWidth={isSelected ? "3" : "2"}
                    className="transition-all duration-200 group-hover:scale-110"
                  />
                  {isSupplier ? (
                    <Factory className="w-5 h-5 text-indigo-400 -translate-x-2.5 -translate-y-2.5 pointer-events-none" />
                  ) : (
                    <Warehouse className={`w-5 h-5 ${isCritical ? "text-rose-400" : "text-cyan-400"} -translate-x-2.5 -translate-y-2.5 pointer-events-none`} />
                  )}

                  {/* Node Label Text */}
                  <text
                    x="0"
                    y="36"
                    textAnchor="middle"
                    fill="#F1F5F9"
                    fontSize="11"
                    fontWeight="bold"
                    className="select-none font-mono"
                  >
                    {n.code}
                  </text>
                  <text
                    x="0"
                    y="50"
                    textAnchor="middle"
                    fill={isCritical ? "#F87171" : "#94A3B8"}
                    fontSize="10"
                    className="select-none"
                  >
                    {n.onHand}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Selected Node Details Drawer */}
        {selectedNode && (
          <div className="mt-4 p-4 rounded-xl bg-command-900 border border-cyan-500/30 flex flex-col md:flex-row md:items-center justify-between gap-3 animate-fadeIn">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                <Layers className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="text-sm font-bold text-white font-mono">{selectedNode.name}</h4>
                  <Badge variant="cyan" size="sm">{selectedNode.code}</Badge>
                  <Badge variant="outline" size="sm">{selectedNode.type}</Badge>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Node telemetry: Real-time inventory tracking and multi-echelon routing status.
                </p>
              </div>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-xs text-slate-400 hover:text-white px-3 py-1 rounded bg-command-800 border border-white/[0.08]"
            >
              Close Details
            </button>
          </div>
        )}
      </Card>
    </div>
  );
}

