"""
Capture 1920x1080 official video thumbnail from slide_thumbnail.html
"""

import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    slide_path = os.path.abspath("docs/recruiter_video/slides/slide_thumbnail.html")
    out_thumb = os.path.abspath("docs/recruiter_video/thumbnail.png")
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(f"file:///{slide_path.replace(os.sep, '/')}")
        await asyncio.sleep(1)
        await page.screenshot(path=out_thumb, full_page=False)
        await browser.close()
    
    print(f"Generated official video thumbnail: {out_thumb} ({os.path.getsize(out_thumb)} bytes)")

if __name__ == "__main__":
    asyncio.run(main())
