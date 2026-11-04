"""
Test recording a live scene from saras-atlas.vercel.app and muxing with audio.
"""

import asyncio
import os
import subprocess
import imageio_ffmpeg
from playwright.async_api import async_playwright

async def record_scene_test():
    output_dir = os.path.abspath("docs/recruiter_video/test_out")
    os.makedirs(output_dir, exist_ok=True)
    temp_video_dir = os.path.join(output_dir, "temp_rec")
    os.makedirs(temp_video_dir, exist_ok=True)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    print("[1] Launching Playwright with Edge...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=edge_path,
            headless=True,
            args=["--disable-gpu", "--no-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=temp_video_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        print("[2] Navigating to https://saras-atlas.vercel.app ...")
        await page.goto("https://saras-atlas.vercel.app", wait_until="networkidle")
        await asyncio.sleep(2)

        # Smooth hover over KPI cards
        print("[3] Performing deliberate mouse hovers...")
        await page.mouse.move(300, 220)
        await asyncio.sleep(1.5)
        await page.mouse.move(600, 220)
        await asyncio.sleep(1.5)
        await page.mouse.move(900, 220)
        await asyncio.sleep(1.5)
        await page.mouse.move(1200, 220)
        await asyncio.sleep(1.5)

        # Scroll down
        print("[4] Scrolling down to inspect alerts...")
        for y in range(0, 400, 20):
            await page.mouse.wheel(0, 20)
            await asyncio.sleep(0.05)
        await asyncio.sleep(2)

        print("[5] Closing context to finish recording...")
        await context.close()
        await browser.close()

    # Find recorded webm
    recorded_files = [os.path.join(temp_video_dir, f) for f in os.listdir(temp_video_dir) if f.endswith(".webm")]
    assert recorded_files, "No webm recorded"
    webm_file = recorded_files[0]
    print(f"[6] WebM recorded: {webm_file} ({os.path.getsize(webm_file)} bytes)")

    # Test muxing with scene_01.mp3
    audio_file = os.path.abspath("docs/recruiter_video/audio/scene_01.mp3")
    out_mp4 = os.path.join(output_dir, "test_scene_01_muxed.mp4")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # Mux: loop video to match audio length, encode to h264 Full HD 30fps
    cmd = [
        ffmpeg, "-y",
        "-stream_loop", "-1",
        "-i", webm_file,
        "-i", audio_file,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-shortest",
        "-c:a", "aac",
        "-b:a", "192k",
        out_mp4
    ]
    print(f"[7] Running FFmpeg mux: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"[8] Finished! Output MP4: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

if __name__ == "__main__":
    asyncio.run(record_scene_test())
