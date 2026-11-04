"""
SARAS ATLAS - Audio & Subtitle Generation Engine
Generates ultra-high-quality Microsoft Neural TTS voiceover for both the full-length
product demonstration (~12-14 min) and the short recruiter highlight (~100 sec).
Outputs audio files, .srt / .vtt subtitle files, and audio_manifest.json with exact durations.
"""

import asyncio
import json
import os
import subprocess
import edge_tts
import imageio_ffmpeg

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
VOLUME = "+0%"

FULL_SCENES = [
    {
        "id": "scene_00",
        "title": "Opening & Problem Formulation",
        "type": "graphic",
        "text": (
            "Hello, and welcome. My name is Srikanth Banoth, and today I am demonstrating SARAS ATLAS—a full-stack "
            "commerce resilience and decision intelligence platform. Modern omnichannel commerce businesses operate "
            "across complex networks of overseas suppliers, cross-dock facilities, regional fulfillment centers, "
            "and volatile consumer demand. In this environment, a single supply chain disruption—such as a delayed factory "
            "shipment or port congestion—does not stay isolated. It triggers a cascading failure: inventory runs dry, "
            "fulfillment centers spill orders across high-cost shipping zones, digital marketing spend continues driving traffic "
            "to empty product pages, and customer satisfaction drops. Traditional business intelligence dashboards are "
            "fundamentally backward-looking: they tell executives what happened yesterday. But when a crisis hits, operators "
            "need answers to six critical forward-looking questions: Why did this disruption occur? What will happen across "
            "our nodes over the next thirty days? What is our exact financial exposure? What is the mathematically optimal "
            "corrective action? How much capital will that intervention require? And who holds governance authority to approve it? "
            "SARAS ATLAS was engineered to connect these questions into a single, closed-loop decision workflow. Before we dive into "
            "the live application, a brief disclosure: this is an independent portfolio project demonstrated on synthetic commerce "
            "data representing Vanguard Apparel Company, a forty-five million dollar apparel merchant. It is not affiliated with or "
            "endorsed by Saras Analytics. Let us now open the live production application deployed at saras-atlas.vercel.app."
        )
    },
    {
        "id": "scene_01",
        "title": "Executive Command Center",
        "type": "live",
        "tab": "situation_room",
        "text": (
            "Here on the live production application, we land on the Executive Command Center. Rather than overwhelming "
            "leadership with raw telemetry, the command center aggregates high-level operational and financial health into four "
            "primary indicators. At the top left, we immediately see our total active commercial exposure: two hundred twenty-four "
            "thousand, five hundred dollars. Next to it, the platform surfaces the net contribution margin at risk—one hundred "
            "twenty-nine thousand, eight hundred forty-four dollars and thirty-two cents. Notice how the interface immediately "
            "distinguishes between top-line revenue exposed and true bottom-line margin erosion. The system signals an active supply "
            "chain bottleneck, with overall network resilience tracked at eighty-eight point four percent. Below the metrics, real-time "
            "alerts pinpoint active purchase order anomalies, supplier delays, and inventory thresholds across our distribution nodes."
        )
    },
    {
        "id": "scene_02",
        "title": "Digital Twin & Network Topology",
        "type": "live",
        "tab": "digital_twin",
        "text": (
            "To understand where vulnerabilities lie, we move to the Digital Twin and Network Topology view. Here, the platform models "
            "Vanguard Apparel's physical supply chain as a directed graph. In this synthetic business scenario, tier-one manufacturing "
            "partners in Ningbo and Ho Chi Minh City ship finished apparel across ocean corridors into the Port of Los Angeles. From there, "
            "inventory flows inland to our Central Distribution Center in Dallas, Texas, which replenishes regional fulfillment centers in "
            "Allentown, Pennsylvania, and Reno, Nevada. Every node tracks holding capacity, inbound velocity, lead-time variance, and handling "
            "unit costs. By modeling the relationships between suppliers, purchase orders, and multi-echelon stock points, SARAS ATLAS can simulate "
            "how a shock at the supplier tier propagates downstream into fulfillment zones."
        )
    },
    {
        "id": "scene_03",
        "title": "Operational Risk Monitoring",
        "type": "live",
        "tab": "risks",
        "text": (
            "Moving to Risk Monitoring, SARAS ATLAS tracks leading operational risk indicators before they manifest as customer stockouts. "
            "In our supplier scorecard, our primary vendor, Pacific Mills, has breached safety tolerances with an average lead-time variance "
            "of plus-twenty-one days. The platform calculates a composite supplier reliability index based on on-time in-full delivery rates, "
            "ocean transit dwell times, and customs clearance volatility. Notice that while domestic vendors like Nordic Fleece remain stable, "
            "Pacific Mills is flagged in high-risk red. The system alerts us that Purchase Order PO-9012—containing five thousand units of "
            "our flagship Performance Heather Tees—is stalled at port, directly threatening our fourth-quarter peak sales volume."
        )
    },
    {
        "id": "scene_04",
        "title": "Root Cause Analysis & Loss Attribution",
        "type": "live",
        "tab": "rca",
        "text": (
            "When an alert fires, operators don't need raw guesswork; they need Root Cause Analysis. The RCA engine breaks down the total "
            "two hundred twenty-four thousand, five hundred dollar commercial exposure into five mutually exclusive, collectively exhaustive "
            "loss categories: First, Direct Stockout Losses: ninety-eight thousand, seven hundred eighty dollars in unfulfilled consumer demand. "
            "Second, Expedited Maritime Surcharges: fifty-four thousand dollars in detention, demurrage, and emergency container priority fees. "
            "Third, Cross-Zone Spillover: forty-five thousand, six hundred twenty dollars incurred when our East Hub stocks out, forcing West Hub "
            "to ship across country at peak parcel rates. Fourth, Ad Spend Burn: eighteen thousand, one hundred dollars in digital advertising "
            "dollars that continue bidding on out-of-stock SKUs with zero conversion. And fifth, Split-Order Handling: eight thousand dollars "
            "in warehouse pick-pack penalties for multi-item baskets split across facilities. Every dollar is mathematically attributed to "
            "PO-9012's twenty-one-day supplier slip."
        )
    },
    {
        "id": "scene_05",
        "title": "Predictive Demand Forecasting",
        "type": "live",
        "tab": "forecasting",
        "text": (
            "Accurate loss calculation requires rigorous Demand Forecasting. In the forecasting studio, SARAS ATLAS evaluates baseline sales "
            "velocity across daily, weekly, and promotional cadences. Rather than using toy moving averages, the platform implements two distinct "
            "statistical models: an additive Holt-Winters Triple Exponential Smoothing engine for seasonal capture, and an L2-regularized Ridge "
            "regression model incorporating price elasticity and promotional flags. The system evaluates model performance using Weighted Absolute "
            "Percentage Error—or WAPE—achieving eleven point eight percent on the active SKU. By generating probabilistic demand bounds with "
            "eighty percent and ninety-five percent confidence bands, the system feeds realistic, risk-adjusted demand projections directly into "
            "downstream inventory and optimization models."
        )
    },
    {
        "id": "scene_06",
        "title": "Inventory Levels & Stockout Dynamics",
        "type": "live",
        "tab": "digital_twin",
        "text": (
            "Now let us examine the Inventory Dynamics. Here we see the multi-echelon stock trajectory for SKU-001. Under normal conditions, "
            "our safety stock buffer maintains twelve hundred units at Dallas Central. However, with PO-9012 delayed by twenty-one days, "
            "current inventory is depleting at one hundred twelve units per day. The platform calculates that Dallas Central will completely breach "
            "safety stock within four days and hit hard stockout in exactly nine days. Once Dallas stocks out, regional hubs deplete their local "
            "buffers, triggering the cross-zone shipping surcharges and stockouts we saw in the RCA module. Time is of the essence."
        )
    },
    {
        "id": "scene_07",
        "title": "Disruption Simulation Studio",
        "type": "live",
        "tab": "simulation",
        "text": (
            "Before committing capital, supply chain directors can run What-If Disruption Simulations. The simulator lets operators test "
            "scenarios dynamically. If Pacific Mills slips by twenty-eight days instead of twenty-one, financial exposure jumps from two hundred "
            "twenty-four thousand dollars to over two hundred ninety thousand dollars. Conversely, if consumer demand cools by ten percent, "
            "our existing inventory buffer extends our stockout runway by five critical days. This interactive simulation engine enables leadership "
            "to stress-test their operational resilience against severe macro volatility before deciding on an intervention."
        )
    },
    {
        "id": "scene_08",
        "title": "The Mathematical Optimization Engine",
        "type": "live",
        "tab": "optimization",
        "text": (
            "Now we arrive at the intellectual core of SARAS ATLAS: Mathematical Optimization. Faced with a stockout, most companies rely on "
            "rules of thumb or intuition. SARAS ATLAS formulates the mitigation decision as a rigorous Mixed-Integer Linear Program, solved using "
            "Google OR-Tools and the SCIP solver. Let us look at the problem formulation: We have two transport levers: expedited air freight at "
            "twelve dollars and fifty cents per unit, which yields fifty-eight dollars and eighty-three cents in net contribution margin, and expedited "
            "ground transfer from our secondary hub at three dollars and twenty cents per unit, which yields eighty-one dollars and thirteen cents in "
            "net margin. We face a strict working-capital budget of forty thousand dollars, and ground inventory is physically capped at eight hundred "
            "available units. Notice what the solver does: Because ground transfer provides a higher return on capital—delivering over twenty-five dollars "
            "of margin per dollar spent—the solver exhausts the entire eight hundred-unit ground capacity first, consuming two thousand five hundred sixty dollars. "
            "With the remaining thirty-seven thousand four hundred forty dollars of budget, it allocates capital to expedited air freight at twelve-fifty "
            "per unit. Thirty-seven thousand four hundred forty divided by twelve-fifty equals twenty-nine ninety-five point two units. Because air freight "
            "must be booked in integer units, the solver commits to exactly two thousand nine hundred ninety-five air units, spending thirty-seven thousand "
            "four hundred thirty-seven dollars and fifty cents. Total capital expenditure: thirty-nine thousand, nine hundred ninety-seven dollars and fifty cents. "
            "Remaining budget slack: exactly two dollars and fifty cents—because two dollars and fifty cents cannot purchase another twelve-dollar-fifty "
            "air freight unit. Ad throttling remains at zero percent because maintaining full marketing velocity is more profitable than throttling spend "
            "once inventory is replenished. This is not heuristic guessing; this is provably optimal mathematical decision-making."
        )
    },
    {
        "id": "scene_09",
        "title": "Financial Waterfall & Margin Reconciliation",
        "type": "live",
        "tab": "waterfall",
        "text": (
            "A frequent trap in supply chain leadership is conflating gross revenue with net profitability. In our Financial Waterfall and "
            "Reconciliation module, SARAS ATLAS ensures total accounting precision. While gross commercial exposure is two hundred twenty-four thousand, "
            "five hundred dollars, unfulfilled customer orders mean the company avoids paying variable inventory cost of goods sold and final-mile "
            "parcel shipping fees totaling ninety-four thousand, six hundred fifty-five dollars and sixty-eight cents. Subtracting those avoided costs "
            "reveals our true net contribution margin erosion: one hundred twenty-nine thousand, eight hundred forty-four dollars and thirty-two cents. "
            "By spending thirty-nine thousand, nine hundred ninety-seven dollars and fifty cents on our SCIP-optimized mitigation plan, we fully protect "
            "this one hundred twenty-nine thousand, eight hundred forty-four dollars of contribution margin—generating an immediate three point two five "
            "X return on invested working capital. This level of clarity gives CFOs complete confidence in operational expenditures."
        )
    },
    {
        "id": "scene_10",
        "title": "Governance & Two-Man Rule Approval",
        "type": "live",
        "tab": "governance",
        "text": (
            "High-value algorithmic decisions cannot be deployed into production without governance. In the Governance and Approval module, "
            "SARAS ATLAS enforces institutional accountability. Our corporate policy establishes a twenty-five thousand dollar working-capital "
            "approval threshold. Because our optimized mitigation outlay is thirty-nine thousand, nine hundred ninety-seven dollars and fifty cents, "
            "the platform automatically triggers the Two-Man Rule. First, the Supply Chain Director reviews the operational allocation and signs. "
            "But the order cannot execute until an independent second officer—in this case, the VP of Finance—reviews the financial reconciliation "
            "and countersigns. Each action is stamped with an immutable, auditable log including timestamps, role-based access verification, and "
            "cryptographic SHA-256 digital signature hashes. Algorithms recommend; human leaders govern."
        )
    },
    {
        "id": "scene_11",
        "title": "Executive Reporting & Parity Export",
        "type": "live",
        "tab": "reports",
        "text": (
            "Finally, the Executive Reporting module bridges technical optimization and boardroom communication. With a single click, operators "
            "can generate executive-ready PDF briefs and CSV audit packages. The generated PDF contains the full disruption summary, root-cause "
            "loss breakdown, reconciled financial waterfall, mathematical solver parameters, and the countersigned governance audit trail. "
            "Perfect parity between the web dashboard, PDF exports, and raw CSV files guarantees that leadership, finance, and logistics operate "
            "on a single source of truth."
        )
    },
    {
        "id": "scene_12",
        "title": "What Makes SARAS ATLAS Different?",
        "type": "graphic",
        "text": (
            "So, what truly sets SARAS ATLAS apart from conventional enterprise dashboards? Most business intelligence tools are purely descriptive: "
            "they look in the rearview mirror and tell you what broke. SARAS ATLAS provides an end-to-end prescriptive decision loop. We differentiate "
            "across seven core engineering pillars: One: Unified Decision Workflow—connecting monitoring, root-cause analysis, simulation, and execution "
            "into one continuous thread. Two: Financially Grounded Metrics—translating disruptions into gross exposure, avoided costs, and net contribution "
            "margin. Three: Constrained Mathematical Optimization—using Mixed-Integer Linear Programming to guarantee optimality under physical and capital "
            "limits. Four: Algorithmic Explainability—making solver choices clear with shadow prices and marginal efficiency rankings. Five: Institutional "
            "Governance—automated Two-Man Rule dual approvals under corporate limits. Six: Executive Communication—instant parity across dashboards, PDFs, "
            "and CSVs. And Seven: End-to-End Systems Engineering—a modern, tightly integrated full-stack architecture that operates with complete resource efficiency."
        )
    },
    {
        "id": "scene_13",
        "title": "Technical Architecture & Tech Stack",
        "type": "graphic",
        "text": (
            "Let us look under the hood at the technical architecture. SARAS ATLAS is engineered as an in-process modular monolith, prioritizing "
            "operational simplicity, zero network serialization latency between services, and strict resource efficiency. On the frontend, we utilize "
            "Next.js fifteen with the React nineteen App Router and TypeScript, styled with Tailwind CSS. The UI runs on Vercel's Edge Network, where reverse-proxy "
            "rewrite rules route all API traffic through a single origin, completely eliminating cross-origin resource sharing overhead and browser preflight latencies. "
            "On the backend, we run Python 3.12 and FastAPI, with Pydantic version two providing strict schema validation. For storage, we use SQLite in Write-Ahead "
            "Logging mode for zero-latency concurrent transactional reads and writes, paired with DuckDB for lightning-fast columnar analytical queries on synthetic "
            "order logs. The optimization core leverages Google OR-Tools binding the SCIP solver, delivering integer optimal solutions in under fifteen milliseconds. "
            "Forecasting utilizes NumPy and Scikit-Learn for regularized regression and smoothing. Remarkably, this entire backend—including database, solver, and API layers—"
            "operates with a memory footprint of just fifty megabytes of RAM, comfortably under our three hundred fifty megabyte budget and running on a strict zero-dollar cloud tier."
        )
    },
    {
        "id": "scene_14",
        "title": "Executive Business Value & Decision ROI",
        "type": "graphic",
        "text": (
            "What is the tangible business value of this platform to an executive? In traditional retail organizations, diagnosing a supplier delay "
            "and coordinating mitigation across supply chain, merchandising, marketing, and finance takes between three and five days of email chains "
            "and spreadsheet reconciliations. By the time leadership agrees on an air-freight budget, stockouts have already occurred. SARAS ATLAS "
            "compresses that multi-day decision cycle into less than ten minutes: Risk is detected twenty-one days before arrival. Financial exposure "
            "is quantified with exact margin precision. Mitigation is optimized to maximize capital efficiency—delivering a three point two five X "
            "return on invested working capital. And governance approvals are completed digitally with a permanent audit trail. In an industry where operating "
            "margins are fiercely contested, transforming reactive fire-fighting into proactive decision intelligence is the ultimate competitive advantage."
        )
    },
    {
        "id": "scene_15",
        "title": "Personal Project Ownership & Closing",
        "type": "graphic",
        "text": (
            "SARAS ATLAS is an independently architected and implemented portfolio project. Every component you have seen today—from the Next.js frontend "
            "and responsive visualization components, to the FastAPI backend, the SCIP mathematical formulation, the financial waterfall algorithms, the synthetic "
            "data generator, and the cloud deployment pipeline—was built from the ground up to demonstrate production-grade software craftsmanship. It reflects my "
            "conviction that data science and artificial intelligence achieve their greatest value when they are not kept in isolated research notebooks, but "
            "embedded directly into robust, beautifully engineered software that empowers human leaders to make superior decisions. SARAS ATLAS demonstrates how "
            "data engineering, analytics, mathematical optimization, and software engineering can come together to support better operational decisions. "
            "You can explore the live application at saras-atlas.vercel.app, or inspect the open-source codebase, test suites, and technical documentation on GitHub at "
            "github.com/Srikanthbanoth7533/saras-atlas. Thank you very much for your time and consideration."
        )
    }
]

SHORT_SCENES = [
    {
        "id": "short_01",
        "title": "Hook & Executive Overview",
        "text": (
            "Hi, I am Srikanth Banoth, and this is SARAS ATLAS—a commerce resilience and decision intelligence platform that turns supply chain disruptions "
            "into mathematically optimized, financially reconciled decisions."
        )
    },
    {
        "id": "short_02",
        "title": "Disruption & Root Cause Analysis",
        "text": (
            "In our synthetic scenario, a twenty-one-day supplier delay threatens five thousand units of inventory. Rather than just reporting lost sales, "
            "ATLAS decomposes our total two hundred twenty-four thousand, five hundred dollar gross exposure into five distinct root causes—including maritime "
            "surcharges, cross-zone shipping spillovers, and wasted digital ad burn."
        )
    },
    {
        "id": "short_03",
        "title": "SCIP Optimization Engine",
        "text": (
            "To mitigate the crisis, we formulate a Mixed-Integer Linear Program solved with Google OR-Tools and SCIP. Under a strict forty thousand dollar "
            "capital budget, the solver proves the optimal policy: exhaust eight hundred units of cheap ground transfer, allocate two thousand nine hundred "
            "ninety-five units of air freight, and retain full ad velocity, investing thirty-nine thousand, nine hundred ninety-seven dollars and fifty cents "
            "with just two dollars and fifty cents in budget slack."
        )
    },
    {
        "id": "short_04",
        "title": "Financial Waterfall & Two-Man Governance",
        "text": (
            "Our financial waterfall reconciles gross revenue against ninety-four thousand, six hundred dollars of avoided variable costs, protecting "
            "one hundred twenty-nine thousand, eight hundred forty-four dollars of true net contribution margin—a three point two five X ROI. And because "
            "capital exceeds twenty-five thousand dollars, our Two-Man Rule requires cryptographic dual-officer sign-off before execution."
        )
    },
    {
        "id": "short_05",
        "title": "Architecture & Closing",
        "text": (
            "Built with Next.js fifteen, FastAPI, DuckDB, SQLite WAL, and OR-Tools, the entire backend runs on less than fifty megabytes of RAM. "
            "Check out the live application at saras-atlas.vercel.app or inspect the open-source codebase on GitHub. Thank you!"
        )
    }
]

def get_audio_duration(file_path: str) -> float:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    res = subprocess.run([ffmpeg, "-i", file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 00:01:23.45, start: 0.000000...
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0

def sec_to_srt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

async def generate_scene_audio(scene: dict, output_dir: str):
    audio_path = os.path.join(output_dir, f"{scene['id']}.mp3")
    vtt_path = os.path.join(output_dir, f"{scene['id']}.vtt")
    communicate = edge_tts.Communicate(scene["text"], VOICE, rate=RATE, volume=VOLUME)
    await communicate.save(audio_path)
    dur = get_audio_duration(audio_path)
    scene["audio_path"] = audio_path
    scene["duration"] = round(dur, 2)
    print(f"Generated {scene['id']}: {dur:.2f}s -> {scene['title']}")
    return scene

async def main():
    base_dir = os.path.abspath("docs/recruiter_video")
    audio_dir = os.path.join(base_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    print("=== Generating Full Walkthrough Audio (16 Scenes) ===")
    full_manifest = []
    current_time = 0.0
    master_srt_lines = []
    srt_idx = 1

    for scene in FULL_SCENES:
        res = await generate_scene_audio(scene, audio_dir)
        start_time = current_time
        end_time = current_time + res["duration"]
        res["start_time"] = round(start_time, 2)
        res["end_time"] = round(end_time, 2)
        full_manifest.append(res)

        # Chunk text into subtitle blocks of ~12-16 words
        words = res["text"].split()
        chunk_size = 12
        num_chunks = max(1, len(words) // chunk_size + (1 if len(words) % chunk_size else 0))
        chunk_dur = res["duration"] / num_chunks
        for i in range(num_chunks):
            c_text = " ".join(words[i * chunk_size : (i + 1) * chunk_size])
            c_start = start_time + i * chunk_dur
            c_end = start_time + (i + 1) * chunk_dur
            master_srt_lines.append(f"{srt_idx}\n{sec_to_srt_time(c_start)} --> {sec_to_srt_time(c_end)}\n{c_text}\n")
            srt_idx += 1

        current_time = end_time

    total_full_duration = current_time
    print(f"\nTotal Full Demonstration Duration: {total_full_duration:.2f}s ({total_full_duration/60:.2f} min)")

    # Save Full SRT
    full_srt_path = os.path.join(base_dir, "saras_atlas_full_walkthrough.srt")
    with open(full_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(master_srt_lines))
    print(f"Saved full subtitle file: {full_srt_path}")

    # Save Full Manifest
    manifest_path = os.path.join(base_dir, "audio_manifest_full.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(full_manifest, f, indent=2)
    print(f"Saved full audio manifest: {manifest_path}")

    print("\n=== Generating Short Recruiter Highlight Audio (5 Scenes) ===")
    short_manifest = []
    short_current_time = 0.0
    short_srt_lines = []
    short_srt_idx = 1

    for scene in SHORT_SCENES:
        res = await generate_scene_audio(scene, audio_dir)
        start_time = short_current_time
        end_time = short_current_time + res["duration"]
        res["start_time"] = round(start_time, 2)
        res["end_time"] = round(end_time, 2)
        short_manifest.append(res)

        words = res["text"].split()
        chunk_size = 10
        num_chunks = max(1, len(words) // chunk_size + (1 if len(words) % chunk_size else 0))
        chunk_dur = res["duration"] / num_chunks
        for i in range(num_chunks):
            c_text = " ".join(words[i * chunk_size : (i + 1) * chunk_size])
            c_start = start_time + i * chunk_dur
            c_end = start_time + (i + 1) * chunk_dur
            short_srt_lines.append(f"{short_srt_idx}\n{sec_to_srt_time(c_start)} --> {sec_to_srt_time(c_end)}\n{c_text}\n")
            short_srt_idx += 1

        short_current_time = end_time

    total_short_duration = short_current_time
    print(f"\nTotal Short Recruiter Video Duration: {total_short_duration:.2f}s ({total_short_duration/60:.2f} min)")

    # Save Short SRT
    short_srt_path = os.path.join(base_dir, "saras_atlas_recruiter_highlight.srt")
    with open(short_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(short_srt_lines))
    print(f"Saved short subtitle file: {short_srt_path}")

    # Save Short Manifest
    short_manifest_path = os.path.join(base_dir, "audio_manifest_short.json")
    with open(short_manifest_path, "w", encoding="utf-8") as f:
        json.dump(short_manifest, f, indent=2)
    print(f"Saved short audio manifest: {short_manifest_path}")

if __name__ == "__main__":
    asyncio.run(main())
