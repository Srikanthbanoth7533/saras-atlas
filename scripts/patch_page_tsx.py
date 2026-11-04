"""
Integrate ProductOverviewModal and GuidedDemoModal into frontend/src/app/page.tsx
"""

def patch_page():
    path = "frontend/src/app/page.tsx"
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Add imports
    import_target = 'import EnterpriseConnectors from "@/components/modules/EnterpriseConnectors";'
    new_imports = (
        'import EnterpriseConnectors from "@/components/modules/EnterpriseConnectors";\n'
        'import { ProductOverviewModal } from "@/components/layout/ProductOverviewModal";\n'
        'import { GuidedDemoModal } from "@/components/demo/GuidedDemoModal";'
    )
    if import_target in c and "ProductOverviewModal" not in c:
        c = c.replace(import_target, new_imports)

    # 2. Add state
    state_target = 'const [activeTab, setActiveTab] = useState<ActiveTab>("situation_room");'
    new_state = (
        'const [activeTab, setActiveTab] = useState<ActiveTab>("situation_room");\n'
        '  const [isOverviewOpen, setIsOverviewOpen] = useState(false);\n'
        '  const [isDemoOpen, setIsDemoOpen] = useState(false);'
    )
    if state_target in c and "isOverviewOpen" not in c:
        c = c.replace(state_target, new_state)

    # 3. Update Header call
    header_target = '<Header health={health} onRefresh={loadInitialData} isRefreshing={isRefreshing} />'
    new_header = (
        '<Header\n'
        '        health={health}\n'
        '        onRefresh={loadInitialData}\n'
        '        isRefreshing={isRefreshing}\n'
        '        onOpenOverview={() => setIsOverviewOpen(true)}\n'
        '        onOpenDemo={() => setIsDemoOpen(true)}\n'
        '      />'
    )
    if header_target in c:
        c = c.replace(header_target, new_header)

    # 4. Add Modals before closing </div>
    footer_target = """      {/* Platform Status Footer */}
      <footer className="border-t border-white/[0.06] bg-command-950 py-3 px-6 text-center text-xs text-slate-500 font-mono">
        SARAS ATLAS Enterprise Intelligence Platform • Zero-Cost Local Monolith • Target RAM &lt; 350 MB RSS • Vanguard Apparel Co. Benchmark
      </footer>
    </div>"""

    new_footer = """      {/* Platform Status Footer */}
      <footer className="border-t border-white/[0.06] bg-command-950 py-3 px-6 text-center text-xs text-slate-500 font-mono">
        SARAS ATLAS Enterprise Intelligence Platform • Zero-Cost Local Monolith • Target RAM &lt; 350 MB RSS • Vanguard Apparel Co. Benchmark
      </footer>

      {/* Enterprise Product Overview & Identity Modal */}
      <ProductOverviewModal
        isOpen={isOverviewOpen}
        onClose={() => setIsOverviewOpen(false)}
        onNavigateTab={handleTabChange}
        onStartGuidedDemo={() => setIsDemoOpen(true)}
      />

      {/* Guided Executive Demonstration Tour */}
      <GuidedDemoModal
        isOpen={isDemoOpen}
        onClose={() => setIsDemoOpen(false)}
        activeTab={activeTab}
        onNavigateTab={handleTabChange}
      />
    </div>"""

    if footer_target in c:
        c = c.replace(footer_target, new_footer)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("frontend/src/app/page.tsx updated successfully")

if __name__ == "__main__":
    patch_page()
