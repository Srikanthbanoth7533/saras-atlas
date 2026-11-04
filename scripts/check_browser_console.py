"""
SARAS ATLAS - Deep CDP Browser Console Audit
Connects to headless Microsoft Edge via CDP WebSocket, navigates to https://saras-atlas.vercel.app,
and intercepts all Console events, JS exceptions, and network errors.
"""

import asyncio
import subprocess
import time
import json
import urllib.request
import websockets
import sys

async def audit_browser():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    port = 9222
    
    print("[1] Launching headless Edge on port 9222...")
    proc = subprocess.Popen([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        f"--remote-debugging-port={port}",
        "about:blank"
    ])
    
    await asyncio.sleep(2)
    
    errors = []
    warnings = []
    logs = []
    
    try:
        # Get target
        req = urllib.request.Request(f"http://127.0.0.1:{port}/json")
        with urllib.request.urlopen(req) as resp:
            targets = json.loads(resp.read().decode())
        
        page_target = next((t for t in targets if t.get("type") == "page"), None)
        assert page_target is not None, "No page target found"
        ws_url = page_target.get("webSocketDebuggerUrl")
        print(f"[2] Connecting to CDP WebSocket: {ws_url}")
        
        async with websockets.connect(ws_url) as ws:
            # Enable domains
            await ws.send(json.dumps({"id": 1, "method": "Console.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Log.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 4, "method": "Page.enable"}))
            
            # Navigate to live production
            print("[3] Navigating to https://saras-atlas.vercel.app ...")
            await ws.send(json.dumps({
                "id": 5,
                "method": "Page.navigate",
                "params": {"url": "https://saras-atlas.vercel.app"}
            }))
            
            # Listen for 6 seconds
            end_time = time.time() + 6
            while time.time() < end_time:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    event = json.loads(msg)
                    method = event.get("method", "")
                    
                    if method == "Runtime.exceptionThrown":
                        details = event.get("params", {}).get("exceptionDetails", {})
                        text = details.get("text", "") + " " + details.get("exception", {}).get("description", "")
                        errors.append(f"JS Exception: {text}")
                    elif method == "Console.messageAdded":
                        msg_obj = event.get("params", {}).get("message", {})
                        level = msg_obj.get("level")
                        text = msg_obj.get("text")
                        if level == "error":
                            errors.append(f"Console Error: {text}")
                        elif level == "warning":
                            warnings.append(f"Console Warning: {text}")
                        else:
                            logs.append(f"Console Log: {text}")
                    elif method == "Log.entryAdded":
                        entry = event.get("params", {}).get("entry", {})
                        level = entry.get("level")
                        text = entry.get("text")
                        if level == "error":
                            errors.append(f"Log Error: {text}")
                        elif level == "warning":
                            warnings.append(f"Log Warning: {text}")
                except asyncio.TimeoutError:
                    pass
                    
    finally:
        print("[4] Cleaning up Edge process...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
            
    print("\n" + "=" * 80)
    print("BROWSER CONSOLE AUDIT RESULTS (LIVE PRODUCTION)")
    print("=" * 80)
    print(f"Total Console Errors:   {len(errors)}")
    print(f"Total Console Warnings: {len(warnings)}")
    print(f"Total Console Logs:     {len(logs)}")
    
    if errors:
        print("\nERRORS DETECTED:")
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("\n[VERIFIED] ZERO CONSOLE ERRORS ON PRODUCTION!")
        
    if warnings:
        print("\nWARNINGS DETECTED:")
        for w in warnings:
            print(f"  [WARN] {w}")

if __name__ == "__main__":
    asyncio.run(audit_browser())
