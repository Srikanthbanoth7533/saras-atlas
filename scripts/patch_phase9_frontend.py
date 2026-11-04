"""
Phase 9 Frontend Text and Precision Updates
"""

def patch_situation_room():
    path = "frontend/src/components/modules/SituationRoom.tsx"
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    
    old_target = '<span className="text-rose-400 font-bold">$290k+ in net contribution margin</span>.'
    new_target = '<span className="text-rose-400 font-bold">$224,500.00 in gross revenue ($129,844.32 net CM erosion)</span>.'
    
    if old_target in c:
        c = c.replace(old_target, new_target)
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        print("Updated SituationRoom.tsx successfully")
    else:
        print("Target already updated or not found in SituationRoom.tsx")

def patch_root_cause():
    path = "frontend/src/components/modules/RootCauseAnalysis.tsx"
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # Enhance top right banner to display both Gross and Net
    old_banner = """          <div className="text-right">
            <span className="text-xs text-slate-400 block">Total Attributed Financial Loss</span>
            <span className="text-2xl font-mono font-bold text-rose-400">
              {data ? `$${data.total_financial_impact.toLocaleString()}` : "$224,500.00"}
            </span>
          </div>"""

    new_banner = """          <div className="text-right space-y-1">
            <div className="flex items-baseline justify-end gap-2">
              <span className="text-xs text-slate-400">Gross Commercial Exposure:</span>
              <span className="text-xl font-mono font-bold text-rose-400">
                {data ? `$${data.total_financial_impact.toLocaleString()}` : "$224,500.00"}
              </span>
            </div>
            <div className="flex items-baseline justify-end gap-2">
              <span className="text-xs text-emerald-400 font-semibold">Net GAAP CM Erosion:</span>
              <span className="text-sm font-mono font-bold text-emerald-400">
                -$129,844.32
              </span>
              <span className="text-[10px] text-slate-400">(Variable Savings: $94,655.68)</span>
            </div>
          </div>"""

    if old_banner in c:
        c = c.replace(old_banner, new_banner)
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        print("Updated RootCauseAnalysis.tsx successfully")
    else:
        print("Target already updated or not found in RootCauseAnalysis.tsx")

if __name__ == "__main__":
    patch_situation_room()
    patch_root_cause()
