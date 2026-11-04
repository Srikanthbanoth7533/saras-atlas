"""
Generates high-definition (1920x1080) presentation slides for non-browser scenes
and the official video thumbnail.
"""

import os

OUTPUT_DIR = os.path.abspath("docs/recruiter_video/slides")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common styling
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px;
    height: 1080px;
    background: radial-gradient(circle at 50% 20%, #0F172A 0%, #070A12 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #F8FAFC;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 60px 80px;
    position: relative;
  }
  .grid-bg {
    position: absolute;
    inset: 0;
    background-image: linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
                      linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
  }
  .glow-cyan {
    text-shadow: 0 0 40px rgba(56, 189, 248, 0.4);
  }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 9999px;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38BDF8;
    font-family: ui-monospace, monospace;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px 28px;
    backdrop-filter: blur(12px);
  }
  .gradient-text {
    background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 60%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .footer-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 24px;
    font-size: 15px;
    color: #64748B;
    font-family: ui-monospace, monospace;
  }
</style>
</head>
<body>
<div class="grid-bg"></div>
"""

FOOT = """
</body>
</html>
"""

# Slide 00: Title & Problem
SLIDE_00 = HEAD + """
  <div style="z-index: 1;">
    <div class="badge">Enterprise Resilience Architecture • Portfolio Demonstration</div>
    <h1 style="font-size: 82px; font-weight: 800; letter-spacing: -0.03em; margin-top: 24px; line-height: 1.05;" class="gradient-text glow-cyan">
      SARAS ATLAS
    </h1>
    <h2 style="font-size: 32px; font-weight: 500; color: #94A3B8; margin-top: 12px; letter-spacing: -0.01em;">
      Commerce Resilience & Decision Intelligence Platform
    </h2>
    <p style="font-size: 20px; color: #38BDF8; margin-top: 12px; font-family: ui-monospace, monospace; letter-spacing: 0.05em;">
      Model operational disruptions • Quantify financial exposure • Optimize mitigation decisions
    </p>
  </div>

  <div style="z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 30px;">
    <div class="card" style="border-left: 4px solid #EF4444;">
      <div style="color: #EF4444; font-family: ui-monospace, monospace; font-size: 13px; font-weight: bold;">DISRUPTION ANATOMY</div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 8px;">Cascading Failures</div>
      <p style="font-size: 15px; color: #94A3B8; margin-top: 8px; line-height: 1.5;">
        A 21-day supplier delay at sea cascades into stockouts, split shipments, expedited parcel fees, and burnt advertising capital.
      </p>
    </div>

    <div class="card" style="border-left: 4px solid #F59E0B;">
      <div style="color: #F59E0B; font-family: ui-monospace, monospace; font-size: 13px; font-weight: bold;">FINANCIAL GROUNDING</div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 8px;">Gross vs. Net Margin</div>
      <p style="font-size: 15px; color: #94A3B8; margin-top: 8px; line-height: 1.5;">
        Reconciling <strong>$224,500</strong> gross revenue exposure against <strong>$94,655</strong> avoided COGS to isolate true <strong>$129,844.32</strong> margin erosion.
      </p>
    </div>

    <div class="card" style="border-left: 4px solid #10B981;">
      <div style="color: #10B981; font-family: ui-monospace, monospace; font-size: 13px; font-weight: bold;">PRESCRIPTIVE OPTIMIZATION</div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 8px;">OR-Tools SCIP MILP</div>
      <p style="font-size: 15px; color: #94A3B8; margin-top: 8px; line-height: 1.5;">
        Mathematically optimal capital allocation under $40,000 budget: 800 ground units + 2,995 air units with $2.50 slack and 3.25x ROI.
      </p>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div><strong>Notice:</strong> Independent portfolio demonstration using synthetic business data. Not affiliated with or endorsed by Saras Analytics.</div>
    <div style="color: #38BDF8;">saras-atlas.vercel.app</div>
  </div>
""" + FOOT

# Slide 12: Differentiators
SLIDE_12 = HEAD + """
  <div style="z-index: 1;">
    <div class="badge">Value Paradigm Shift</div>
    <h1 style="font-size: 64px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px;" class="gradient-text">
      What Makes SARAS ATLAS Different?
    </h1>
    <p style="font-size: 22px; color: #94A3B8; margin-top: 8px;">
      Moving enterprise commerce from passive dashboards to closed-loop prescriptive decision intelligence.
    </p>
  </div>

  <div style="z-index: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 24px;">
    <div class="card">
      <div style="color: #38BDF8; font-size: 28px; font-weight: 800;">01</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Unified Workflow</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Connects monitoring, root-cause tracing, simulation, and execution into one continuous system.
      </div>
    </div>
    <div class="card">
      <div style="color: #38BDF8; font-size: 28px; font-weight: 800;">02</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Financial Grounding</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Distinguishes gross top-line commercial risk from true net contribution margin erosion.
      </div>
    </div>
    <div class="card">
      <div style="color: #38BDF8; font-size: 28px; font-weight: 800;">03</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Mathematical MILP</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Replaces arbitrary heuristics with Google OR-Tools SCIP solver constrained optimization.
      </div>
    </div>
    <div class="card">
      <div style="color: #38BDF8; font-size: 28px; font-weight: 800;">04</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Full Explainability</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Exposes shadow prices, capital efficiency rankings, and exact proofs for remaining budget slack.
      </div>
    </div>
    <div class="card">
      <div style="color: #10B981; font-size: 28px; font-weight: 800;">05</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Two-Man Governance</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Mandates independent dual-officer cryptographic authorization for capital over $25,000.
      </div>
    </div>
    <div class="card">
      <div style="color: #10B981; font-size: 28px; font-weight: 800;">06</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">Executive Parity</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        Instant export parity across web dashboards, publication-grade PDFs, and raw CSV audit trails.
      </div>
    </div>
    <div class="card" style="grid-column: span 2;">
      <div style="color: #10B981; font-size: 28px; font-weight: 800;">07</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">End-to-End Modern Engineering</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
        In-process modular monolith (FastAPI + Next.js 15 + DuckDB + SQLite WAL) operating at &lt; 50 MB RSS RAM on a zero-dollar cloud budget.
      </div>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div>Traditional BI: <em>"What happened yesterday?"</em></div>
    <div style="color: #38BDF8;">SARAS ATLAS: <em>"What happened, why, what's next, what should we do, how much does it cost, and who approves it?"</em></div>
  </div>
""" + FOOT

# Slide 13: Technical Architecture
SLIDE_13 = HEAD + """
  <div style="z-index: 1;">
    <div class="badge">Systems Engineering Blueprint</div>
    <h1 style="font-size: 64px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px;" class="gradient-text">
      Technical Architecture & Stack
    </h1>
    <p style="font-size: 22px; color: #94A3B8; margin-top: 8px;">
      Zero-cost in-process modular monolith delivering sub-15ms solver latency on &lt; 50 MB RAM.
    </p>
  </div>

  <div style="z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 24px;">
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-family: ui-monospace, monospace; color: #38BDF8; font-weight: bold; font-size: 13px;">EDGE CLIENT TIER</span>
        <span style="background: rgba(56,189,248,0.15); color: #38BDF8; font-size: 11px; padding: 2px 8px; border-radius: 4px; font-family: ui-monospace, monospace;">VERCEL</span>
      </div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 10px;">Next.js 15 & React 19</div>
      <ul style="font-size: 14px; color: #94A3B8; margin-top: 12px; line-height: 1.8; list-style-position: inside;">
        <li>App Router with TypeScript & Tailwind CSS</li>
        <li>16 responsive decision & telemetry modules</li>
        <li>Lucide UI + Recharts analytical charts</li>
        <li>Single-origin edge rewrites (Zero-CORS)</li>
      </ul>
    </div>

    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-family: ui-monospace, monospace; color: #818CF8; font-weight: bold; font-size: 13px;">APPLICATION ENGINE</span>
        <span style="background: rgba(129,140,248,0.15); color: #818CF8; font-size: 11px; padding: 2px 8px; border-radius: 4px; font-family: ui-monospace, monospace;">RENDER</span>
      </div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 10px;">Python 3.12 & FastAPI</div>
      <ul style="font-size: 14px; color: #94A3B8; margin-top: 12px; line-height: 1.8; list-style-position: inside;">
        <li>Pydantic v2 strict request/response contracts</li>
        <li>SQLAlchemy 2.0 ORM with connection pooling</li>
        <li>Holt-Winters & Ridge regression demand engine</li>
        <li>ReportLab PDF & CSV executive generators</li>
      </ul>
    </div>

    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-family: ui-monospace, monospace; color: #10B981; font-weight: bold; font-size: 13px;">STORAGE & SOLVER CORE</span>
        <span style="background: rgba(16,185,129,0.15); color: #10B981; font-size: 11px; padding: 2px 8px; border-radius: 4px; font-family: ui-monospace, monospace;">EMBEDDED</span>
      </div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 10px;">OR-Tools SCIP & DuckDB</div>
      <ul style="font-size: 14px; color: #94A3B8; margin-top: 12px; line-height: 1.8; list-style-position: inside;">
        <li>Google OR-Tools SCIP 9.0 integer solver</li>
        <li>SQLite Write-Ahead Logging (WAL) concurrency</li>
        <li>DuckDB in-process columnar analytical engine</li>
        <li>Total Process RSS Memory: <strong>50.0 MB</strong></li>
      </ul>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div>Architecture: In-Process Modular Monolith • Latency: &lt; 15ms • Budget: $0.00 Cloud Tier</div>
    <div style="color: #10B981;">100% Type-Safe & Zero Memory Leaks</div>
  </div>
""" + FOOT

# Slide 14: Business Value
SLIDE_14 = HEAD + """
  <div style="z-index: 1;">
    <div class="badge">Executive Value Analysis</div>
    <h1 style="font-size: 64px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px;" class="gradient-text">
      Quantified Business Value & ROI
    </h1>
    <p style="font-size: 22px; color: #94A3B8; margin-top: 8px;">
      Compressing multi-day cross-functional crisis meetings into 8 minutes of data-driven execution.
    </p>
  </div>

  <div style="z-index: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-top: 30px;">
    <div class="card" style="text-align: center; border-top: 4px solid #38BDF8;">
      <div style="font-size: 48px; font-weight: 800; color: #38BDF8; font-family: ui-monospace, monospace;">-96%</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 10px;">Decision Cycle Time</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px;">From 4 days of siloed emails down to 8 minutes</div>
    </div>

    <div class="card" style="text-align: center; border-top: 4px solid #10B981;">
      <div style="font-size: 48px; font-weight: 800; color: #10B981; font-family: ui-monospace, monospace;">3.25x</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 10px;">Working Capital ROI</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px;">$129.8k margin preserved via $39.9k deployed</div>
    </div>

    <div class="card" style="text-align: center; border-top: 4px solid #F59E0B;">
      <div style="font-size: 48px; font-weight: 800; color: #F59E0B; font-family: ui-monospace, monospace;">+21d</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 10px;">Early Proactive Buffer</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px;">Detecting supply slips before vessel arrival</div>
    </div>

    <div class="card" style="text-align: center; border-top: 4px solid #818CF8;">
      <div style="font-size: 48px; font-weight: 800; color: #818CF8; font-family: ui-monospace, monospace;">100%</div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 10px;">Governance Auditability</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 6px;">Cryptographic dual-key approval on high outlays</div>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div>Synthetic Benchmark: Vanguard Apparel Co. ($45M Annual Omnichannel GMV)</div>
    <div style="color: #38BDF8;">From Reactive Firefighting to Prescriptive Intelligence</div>
  </div>
""" + FOOT

# Slide 15: Closing & Portfolio Contact
SLIDE_15 = HEAD + """
  <div style="z-index: 1; text-align: center; max-width: 1200px; margin: 0 auto;">
    <div class="badge">Independent Engineering Portfolio</div>
    <h1 style="font-size: 72px; font-weight: 800; letter-spacing: -0.03em; margin-top: 24px;" class="gradient-text glow-cyan">
      SARAS ATLAS
    </h1>
    <h2 style="font-size: 28px; font-weight: 500; color: #94A3B8; margin-top: 12px;">
      Developed & Implemented by <strong>Srikanth Banoth</strong>
    </h2>
    <p style="font-size: 18px; color: #CBD5E1; margin-top: 20px; line-height: 1.6; max-width: 900px; margin-left: auto; margin-right: auto;">
      <em>"SARAS ATLAS demonstrates how data engineering, analytics, mathematical optimization and software engineering can come together to support better operational decisions."</em>
    </p>

    <div style="display: flex; justify-content: center; gap: 30px; margin-top: 40px;">
      <div class="card" style="padding: 24px 36px; text-align: left;">
        <div style="font-size: 13px; color: #38BDF8; font-family: ui-monospace, monospace; font-weight: bold;">LIVE PRODUCTION APP</div>
        <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: #FFFFFF;">https://saras-atlas.vercel.app</div>
      </div>

      <div class="card" style="padding: 24px 36px; text-align: left;">
        <div style="font-size: 13px; color: #10B981; font-family: ui-monospace, monospace; font-weight: bold;">GITHUB REPOSITORY</div>
        <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: #FFFFFF;">github.com/Srikanthbanoth7533/saras-atlas</div>
      </div>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div>Skills: Full-Stack Systems • Mathematical Optimization (SCIP) • Applied ML • Cloud Deployment</div>
    <div style="color: #38BDF8;">Thank You For Your Consideration</div>
  </div>
""" + FOOT

# Slide Thumbnail
SLIDE_THUMBNAIL = HEAD + """
  <div style="z-index: 1;">
    <div style="display: flex; gap: 12px; align-items: center;">
      <div class="badge" style="background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.4); color: #EF4444;">LIVE PRODUCTION WALKTHROUGH</div>
      <div class="badge">NEXT.JS 15 • FASTAPI • SCIP MILP</div>
    </div>
    
    <h1 style="font-size: 96px; font-weight: 900; letter-spacing: -0.04em; margin-top: 24px; line-height: 1.0;" class="gradient-text glow-cyan">
      SARAS ATLAS
    </h1>
    <h2 style="font-size: 38px; font-weight: 600; color: #CBD5E1; margin-top: 16px;">
      Commerce Resilience & Decision Intelligence
    </h2>
    <div style="font-size: 24px; color: #38BDF8; margin-top: 14px; font-family: ui-monospace, monospace;">
      Disruption Simulation • Financial Reconciliation • SCIP Optimization
    </div>
  </div>

  <div style="z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 30px;">
    <div class="card" style="border-left: 4px solid #38BDF8;">
      <div style="font-size: 14px; color: #38BDF8; font-family: ui-monospace, monospace; font-weight: bold;">FINANCIAL RECONCILIATION</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 6px;">$129,844.32</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 4px;">Net Contribution Margin at Risk</div>
    </div>

    <div class="card" style="border-left: 4px solid #10B981;">
      <div style="font-size: 14px; color: #10B981; font-family: ui-monospace, monospace; font-weight: bold;">SCIP OPTIMAL MITIGATION</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 6px;">800 G / 2,995 A</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 4px;">$39,997.50 Outlay • $2.50 Slack</div>
    </div>

    <div class="card" style="border-left: 4px solid #818CF8;">
      <div style="font-size: 14px; color: #818CF8; font-family: ui-monospace, monospace; font-weight: bold;">TWO-MAN GOVERNANCE</div>
      <div style="font-size: 32px; font-weight: 800; margin-top: 6px;">DUAL-KEY APPROVED</div>
      <div style="font-size: 14px; color: #94A3B8; margin-top: 4px;">Cryptographic Audit Trail</div>
    </div>
  </div>

  <div class="footer-bar" style="z-index: 1;">
    <div>Architect & Engineer: Srikanth Banoth</div>
    <div style="color: #38BDF8; font-size: 18px; font-weight: bold;">saras-atlas.vercel.app</div>
  </div>
""" + FOOT

slides = {
    "slide_00_title.html": SLIDE_00,
    "slide_12_differentiators.html": SLIDE_12,
    "slide_13_architecture.html": SLIDE_13,
    "slide_14_business_value.html": SLIDE_14,
    "slide_15_closing.html": SLIDE_15,
    "slide_thumbnail.html": SLIDE_THUMBNAIL
}

for fname, content in slides.items():
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created slide: {fpath}")

print("All graphic presentation slides generated successfully.")
