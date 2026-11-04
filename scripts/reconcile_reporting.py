"""
SARAS ATLAS — Script to Reconcile Executive Reporting Generator (PDF & CSV).
"""

with open("src/domain/reporting/generator.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update executive_summary
old_exec = """            "executive_summary": (
                "An operational bottleneck at Shenzhen consolidation terminals has delayed inbound ocean container PO-9012 "
                "by 21 days with a +28% freight spot surcharge. Without intervention, Vanguard's Los Angeles distribution center "
                "(WH-WEST) will deplete safety stock on Day 34, triggering $224,500 in cumulative EBITDA erosion due to stockouts "
                "and cross-zone Zone 7 shipping bleed. The Google OR-Tools optimization engine prescribes a tri-part mitigation plan "
                "(Air Freight Expedite, Domestic Ground Redistribution, and Ad Throttling) requiring $13,650 in capital to preserve "
                "$148,200 in net contribution margin (10.9x ROI)."
            ),"""

new_exec = """            "executive_summary": (
                "An operational bottleneck at Shenzhen consolidation terminals delayed inbound ocean container PO-9012 "
                "by 21 days with a +28% freight spot surcharge. Without intervention, Vanguard's Los Angeles distribution center "
                "(WH-WEST) depletes safety stock on Day 34, triggering $224,500.00 in unmitigated commercial erosion and "
                "-$129,844.32 in net contribution margin contraction. The Google OR-Tools SCIP optimization engine prescribes a "
                "multi-echelon mitigation plan deploying $39,997.50 in capital (air freight expediting and domestic ground transfer) "
                "to preserve $129,844.32 in net contribution margin (3.25x ROI) and restore customer fill rate to 99.8%."
            ),"""

assert old_exec in text, "old_exec not found"
text = text.replace(old_exec, new_exec)

# 2. Update kpi_posture
old_kpi = """            "kpi_posture": [
                ["Enterprise Metric", "Baseline Target", "Unmitigated Shock", "ATLAS Mitigated", "Variance Lift"],
                ["Net Contribution Margin", "$3,124,500", "$2,900,000", "$3,048,200", "+$148,200 (+5.1%)"],
                ["Customer Order Fill Rate", "98.5%", "84.2%", "96.8%", "+12.6% pts"],
                ["Days of Coverage (WH-WEST)", "30.0 Days", "14.2 Days (Runout D34)", "28.5 Days", "+14.3 Days"],
                ["Cross-Zone Order Spillover", "4.2%", "24.8%", "6.1%", "-18.7% pts"],
                ["Cash Capital Buffer", "$850,000", "$625,500", "$790,850", "+$165,350"],
            ],"""

new_kpi = """            "kpi_posture": [
                ["Enterprise Metric", "Baseline Target", "Unmitigated Shock", "ATLAS Mitigated", "Variance Lift"],
                ["Net Contribution Margin (90d)", "$1,034,977.64", "$905,133.32", "$1,034,977.64", "+$129,844.32 (+14.3%)"],
                ["Customer Order Fill Rate", "99.2%", "87.3%", "99.8%", "+12.5% pts"],
                ["Days of Coverage (WH-WEST)", "30.0 Days", "14.2 Days (Runout D34)", "28.5 Days", "+14.3 Days"],
                ["Cross-Zone Order Spillover", "4.2%", "24.8%", "4.5%", "-20.3% pts"],
                ["Cash Capital Buffer", "$850,000.00", "$625,500.00", "$810,002.50", "+$184,502.50"],
            ],"""

assert old_kpi in text, "old_kpi not found"
text = text.replace(old_kpi, new_kpi)

# 3. Add total reconciled loss row to attributions
old_attr = """            "root_cause_analysis": {
                "primary_cause": rca.primary_root_cause,
                "narrative": rca.root_cause_narrative,
                "attributions": [
                    [seg.segment_name, f"${seg.dollar_impact:,.2f}", f"{seg.percentage_of_total:.1f}%", seg.accounting_category]
                    for seg in rca.financial_attribution
                ],
            },"""

new_attr = """            "root_cause_analysis": {
                "primary_cause": rca.primary_root_cause,
                "narrative": rca.root_cause_narrative,
                "attributions": [
                    [seg.segment_name, f"${seg.dollar_impact:,.2f}", f"{seg.percentage_of_total:.1f}%", seg.accounting_category]
                    for seg in rca.financial_attribution
                ] + [
                    ["TOTAL RECONCILED LOSS", f"${rca.total_financial_impact:,.2f}", "100.0%", "Cumulative Disruption Loss"]
                ],
            },"""

assert old_attr in text, "old_attr not found"
text = text.replace(old_attr, new_attr)

# 4. Update export_csv to include subtitle, executive summary, and digital seal
old_csv = """        writer.writerow(["SARAS ATLAS — ENTERPRISE DECISION INTELLIGENCE REPORT"])
        writer.writerow(["Enterprise", data["enterprise"]])
        writer.writerow(["Generated At", data["generated_at"]])
        writer.writerow([])"""

new_csv = """        writer.writerow(["SARAS ATLAS — ENTERPRISE DECISION INTELLIGENCE REPORT"])
        writer.writerow(["Enterprise", data["enterprise"]])
        writer.writerow(["Subtitle", data["subtitle"]])
        writer.writerow(["Generated At", data["generated_at"]])
        writer.writerow(["Executive Summary", data["executive_summary"]])
        writer.writerow([])"""

assert old_csv in text, "old_csv not found"
text = text.replace(old_csv, new_csv)

old_gov = """        writer.writerow(["SECTION 4: GOVERNANCE SIGN-OFF"])
        writer.writerow(["Mandate", data["governance"]["mandate"]])
        writer.writerow(["Operations Sign-Off", data["governance"]["approver_1"]])
        writer.writerow(["Finance Sign-Off", data["governance"]["approver_2"]])
        writer.writerow([])"""

new_gov = """        writer.writerow(["SECTION 4: GOVERNANCE SIGN-OFF"])
        writer.writerow(["Mandate", data["governance"]["mandate"]])
        writer.writerow(["Operations Sign-Off", data["governance"]["approver_1"]])
        writer.writerow(["Finance Sign-Off", data["governance"]["approver_2"]])
        writer.writerow(["Digital Seal", data["governance"]["digital_seal"]])
        writer.writerow([])"""

assert old_gov in text, "old_gov not found"
text = text.replace(old_gov, new_gov)

with open("src/domain/reporting/generator.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] generator.py reconciled successfully!")
