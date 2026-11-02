import React from "react";
import { cn } from "@/lib/utils";

interface SliderControlProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  unit?: string;
  defaultValue?: number;
  description?: string;
  onChange: (val: number) => void;
  accentColor?: "cyan" | "rose" | "amber" | "indigo" | "emerald";
}

export function SliderControl({
  label,
  value,
  min,
  max,
  step = 1,
  unit = "",
  defaultValue,
  description,
  onChange,
  accentColor = "cyan",
}: SliderControlProps) {
  const percent = ((value - min) / (max - min)) * 100;

  return (
    <div className="bg-command-900/80 border border-white/[0.06] rounded-lg p-3.5 hover:border-slate-700/80 transition-colors">
      <div className="flex items-center justify-between mb-1.5">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            {label}
          </span>
          {description && (
            <p className="text-[11px] text-slate-400 mt-0.5">{description}</p>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="font-mono text-sm font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2 py-0.5 rounded">
            {value}
            {unit}
          </span>
          {defaultValue !== undefined && value !== defaultValue && (
            <button
              onClick={() => onChange(defaultValue)}
              className="text-[10px] text-slate-400 hover:text-slate-200 underline"
              title={`Reset to default (${defaultValue}${unit})`}
            >
              Reset
            </button>
          )}
        </div>
      </div>

      <div className="relative pt-2 pb-1">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full cursor-pointer"
        />
        <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
          <span>{min}{unit}</span>
          {defaultValue !== undefined && (
            <span className="text-slate-400">Def: {defaultValue}{unit}</span>
          )}
          <span>{max}{unit}</span>
        </div>
      </div>
    </div>
  );
}
