"""
SARAS ATLAS - Master Video Recording, Assembly, and Post-Production Engine
Automates real-time 1920x1080 browser interactions on https://saras-atlas.vercel.app,
renders high-resolution graphic presentation slides, muxes synchronized neural narration,
and outputs both the full demonstration and short recruiter highlight MP4 videos.
"""

import asyncio
import json
import os
import shutil
import subprocess
import time
import imageio_ffmpeg
from playwright.async_api import async_playwright

BASE_DIR = os.path.abspath("docs/recruiter_video")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
SLIDES_DIR = os.path.join(BASE_DIR, "slides")
TEMP_DIR = os.path.join(BASE_DIR, "temp_render")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TAB_NAMES = {
    "situation_room": "Situation Room",
    "digital_twin": "Digital Twin",
    "risks": "Risk Sentinels",
    "simulation": "Simulation Studio",
    "comparison": "Scenario Compare",
    "batch": "Batch & Sensitivity",
    "forecasting": "Forecasting Studio",
    "optimization": "Prescriptive MILP",
    "policy": "Policy Optimization",
    "intelligence": "AI Copilot",
    "rca": "Root Cause Trace",
    "waterfall": "Financial Waterfall",
    "reports": "Executive Reports",
    "governance": "Governance & Audit",
    "ingestion": "Data Ingestion",
    "connectors": "Cloud Connectors"
}

GRAPHIC_SLIDES = {
    "scene_00": "slide_00_title.html",
    "scene_12": "slide_12_differentiators.html",
    "scene_13": "slide_13_architecture.html",
    "scene_14": "slide_14_business_value.html",
    "scene_15": "slide_15_closing.html"
}

async def perform_scene_interactions(page, scene_id, tab_id, duration):
    """
    Executes realistic, deliberate, professional interactions on the live site.
    """
    print(f"[{scene_id}] Navigating / preparing tab: {tab_id} ...")
    
    # 1. Switch tab if not already on it
    if tab_id and tab_id != "situation_room":
        label = TAB_NAMES.get(tab_id)
        if label:
            try:
                btn = page.locator(f"button:has-text('{label}')").first
                await btn.click(timeout=3000)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"[{scene_id}] Tab click fallback for {label}: {e}")

    # 2. Scene-specific interactions
    if scene_id == "scene_01":
        # Hover over KPI cards
        await page.mouse.move(300, 220)
        await asyncio.sleep(2)
        await page.mouse.move(600, 220)
        await asyncio.sleep(2)
        await page.mouse.move(900, 220)
        await asyncio.sleep(2)
        # Scroll down to alerts
        for _ in range(8):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_02":
        # Digital Twin: pan across topology
        await page.mouse.move(500, 400)
        await asyncio.sleep(2)
        await page.mouse.move(800, 350)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 40)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_03":
        # Risks: inspect supplier risk table
        await page.mouse.move(400, 320)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_04":
        # RCA: inspect loss bars
        await page.mouse.move(450, 280)
        await asyncio.sleep(2)
        await page.mouse.move(450, 360)
        await asyncio.sleep(2)
        await page.mouse.move(450, 440)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 25)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_05":
        # Forecasting: toggle models or hover chart
        await page.mouse.move(600, 350)
        await asyncio.sleep(2)
        await page.mouse.move(950, 350)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_06":
        # Inventory dynamics: scroll to stock curves
        for _ in range(8):
            await page.mouse.wheel(0, 40)
            await asyncio.sleep(0.3)
        await page.mouse.move(500, 450)
        await asyncio.sleep(3)

    elif scene_id == "scene_07":
        # Simulation: test what-if parameters
        await page.mouse.move(400, 300)
        await asyncio.sleep(2)
        # Try clicking simulate button if visible
        try:
            sim_btn = page.locator("button:has-text('Run Simulation')").first
            if await sim_btn.is_visible():
                await sim_btn.click()
                await asyncio.sleep(2)
        except Exception:
            pass
        for _ in range(6):
            await page.mouse.wheel(0, 25)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_08":
        # Optimization: Click solve optimization if present
        try:
            solve_btn = page.locator("button:has-text('Solve')").first
            if await solve_btn.is_visible():
                await solve_btn.click()
                await asyncio.sleep(2)
        except Exception:
            pass
        # Hover over ground / air results
        await page.mouse.move(400, 320)
        await asyncio.sleep(2)
        await page.mouse.move(800, 320)
        await asyncio.sleep(2)
        for _ in range(8):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(4)

    elif scene_id == "scene_09":
        # Waterfall: inspect waterfall steps
        await page.mouse.move(350, 380)
        await asyncio.sleep(2)
        await page.mouse.move(700, 380)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_10":
        # Governance: inspect Two-Man Rule
        await page.mouse.move(500, 280)
        await asyncio.sleep(2)
        for _ in range(8):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    elif scene_id == "scene_11":
        # Reports: inspect executive report previews
        await page.mouse.move(400, 300)
        await asyncio.sleep(2)
        for _ in range(6):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.3)
        await asyncio.sleep(3)

    else:
        # Generic gentle scroll and dwell
        await page.mouse.move(500, 300)
        await asyncio.sleep(2)
        for _ in range(4):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.5)

async def record_single_scene(p, scene: dict, temp_scene_dir: str):
    scene_id = scene["id"]
    stype = scene.get("type", "live")
    tab_id = scene.get("tab")
    dur = scene["duration"]

    rec_dir = os.path.join(temp_scene_dir, f"rec_{scene_id}")
    os.makedirs(rec_dir, exist_ok=True)

    browser = await p.chromium.launch(
        executable_path=EDGE_PATH,
        headless=True,
        args=["--disable-gpu", "--no-sandbox"]
    )
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=rec_dir,
        record_video_size={"width": 1920, "height": 1080}
    )
    page = await context.new_page()

    if stype == "graphic":
        slide_name = GRAPHIC_SLIDES.get(scene_id, "slide_00_title.html")
        slide_path = os.path.join(SLIDES_DIR, slide_name)
        await page.goto(f"file:///{slide_path.replace(os.sep, '/')}")
        # Subtle gentle movement on graphic slide
        await asyncio.sleep(1)
        await page.mouse.move(960, 500)
        await asyncio.sleep(3)
        await page.mouse.move(960, 600)
        await asyncio.sleep(3)
    else:
        await page.goto("https://saras-atlas.vercel.app", wait_until="networkidle")
        await asyncio.sleep(1.5)
        await perform_scene_interactions(page, scene_id, tab_id, dur)

    await context.close()
    await browser.close()

    webms = [os.path.join(rec_dir, f) for f in os.listdir(rec_dir) if f.endswith(".webm")]
    assert webms, f"No webm found for {scene_id}"
    return webms[0]

def mux_scene(webm_path: str, audio_path: str, output_mp4: str):
    """
    Uses FFmpeg to loop/extend the video to match exact audio duration,
    encoding to Full HD 1080p 30fps H.264 + AAC.
    """
    cmd = [
        FFMPEG, "-y",
        "-stream_loop", "-1",
        "-i", webm_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-shortest",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def concat_scenes(mp4_list: list, output_master_mp4: str):
    """
    Concatenates an ordered list of scene MP4s into a single master MP4.
    """
    concat_txt = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in mp4_list:
            f.write(f"file '{p.replace(os.sep, '/')}'\n")

    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        "-movflags", "+faststart",
        output_master_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def produce_full_video():
    manifest_path = os.path.join(BASE_DIR, "audio_manifest_full.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    print(f"\n==========================================")
    print(f"PRODUCING FULL DEMO VIDEO ({len(scenes)} SCENES)")
    print(f"==========================================")

    scene_mp4s = []
    async with async_playwright() as p:
        for idx, sc in enumerate(scenes):
            sc_id = sc["id"]
            audio_path = os.path.join(AUDIO_DIR, f"{sc_id}.mp3")
            out_scene_mp4 = os.path.join(TEMP_DIR, f"{sc_id}_rendered.mp4")
            print(f"\n[{idx+1}/{len(scenes)}] Recording & Rendering {sc_id}: {sc['title']} ({sc['duration']}s)...")

            # 1. Record WebM
            webm_file = await record_single_scene(p, sc, TEMP_DIR)
            
            # 2. Mux with Audio
            mux_scene(webm_file, audio_path, out_scene_mp4)
            print(f"[{idx+1}/{len(scenes)}] Done: {out_scene_mp4} ({os.path.getsize(out_scene_mp4)} bytes)")
            scene_mp4s.append(out_scene_mp4)

    # 3. Concatenate all scenes into master MP4
    master_out = os.path.join(BASE_DIR, "saras_atlas_full_walkthrough.mp4")
    print(f"\nConcatenating {len(scene_mp4s)} scenes into master full video...")
    concat_scenes(scene_mp4s, master_out)
    print(f"MASTER FULL DEMO READY: {master_out} ({os.path.getsize(master_out)} bytes)")
    return master_out

async def produce_short_video():
    manifest_path = os.path.join(BASE_DIR, "audio_manifest_short.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    print(f"\n==========================================")
    print(f"PRODUCING SHORT RECRUITER HIGHLIGHT ({len(scenes)} SCENES)")
    print(f"==========================================")

    # Map short scenes to visuals
    short_visual_map = {
        "short_01": {"type": "graphic", "slide": "slide_00_title.html"},
        "short_02": {"type": "live", "tab": "rca"},
        "short_03": {"type": "live", "tab": "optimization"},
        "short_04": {"type": "live", "tab": "waterfall"},
        "short_05": {"type": "graphic", "slide": "slide_15_closing.html"}
    }

    scene_mp4s = []
    async with async_playwright() as p:
        for idx, sc in enumerate(scenes):
            sc_id = sc["id"]
            audio_path = os.path.join(AUDIO_DIR, f"{sc_id}.mp3")
            out_scene_mp4 = os.path.join(TEMP_DIR, f"{sc_id}_rendered.mp4")
            vinfo = short_visual_map.get(sc_id, {"type": "live", "tab": "situation_room"})
            sc["type"] = vinfo["type"]
            sc["tab"] = vinfo.get("tab")
            if "slide" in vinfo:
                GRAPHIC_SLIDES[sc_id] = vinfo["slide"]

            print(f"\n[{idx+1}/{len(scenes)}] Recording & Rendering {sc_id}: {sc['title']} ({sc['duration']}s)...")
            webm_file = await record_single_scene(p, sc, TEMP_DIR)
            mux_scene(webm_file, audio_path, out_scene_mp4)
            print(f"[{idx+1}/{len(scenes)}] Done: {out_scene_mp4} ({os.path.getsize(out_scene_mp4)} bytes)")
            scene_mp4s.append(out_scene_mp4)

    master_short = os.path.join(BASE_DIR, "saras_atlas_recruiter_highlight.mp4")
    print(f"\nConcatenating {len(scene_mp4s)} short scenes into master highlight video...")
    concat_scenes(scene_mp4s, master_short)
    print(f"MASTER SHORT HIGHLIGHT READY: {master_short} ({os.path.getsize(master_short)} bytes)")
    return master_short

async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    t0 = time.time()

    full_video = await produce_full_video()
    short_video = await produce_short_video()

    elapsed = time.time() - t0
    print(f"\n==========================================")
    print(f"ALL VIDEOS SUCCESSFULLY GENERATED IN {elapsed:.1f} SECONDS!")
    print(f"Full Walkthrough: {full_video} ({os.path.getsize(full_video):,} bytes)")
    print(f"Short Highlight: {short_video} ({os.path.getsize(short_video):,} bytes)")
    print(f"==========================================")

if __name__ == "__main__":
    asyncio.run(main())
