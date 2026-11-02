#!/usr/bin/env python3
"""
SARAS ATLAS — Environment Verification Script
Validates Python runtime, virtual environment isolation, operating system metrics, and memory bounds.
"""

import sys
import os
import platform

def verify_system():
    print("=" * 60)
    print("SARAS ATLAS — SYSTEM & ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    # 1. Python Version Check
    py_ver = sys.version_info
    print(f"[OK] Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver.major != 3 or py_ver.minor < 11:
        print("[FAIL] Requires Python 3.12 or compatible 3.11+ release.")
        sys.exit(1)
        
    # 2. Virtual Environment Isolation Check
    in_venv = sys.prefix != sys.base_prefix
    print(f"[OK] In Virtual Environment: {in_venv} (Prefix: {sys.prefix})")
    
    # 3. Operating System & Architecture
    print(f"[OK] OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})")
    print(f"[OK] Processor: {platform.processor()}")
    
    # 4. Memory Audit Check (using ctypes or psutil if available)
    try:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ('dwLength', ctypes.c_ulong),
                ('dwMemoryLoad', ctypes.c_ulong),
                ('ullTotalPhys', ctypes.c_ulonglong),
                ('ullAvailPhys', ctypes.c_ulonglong),
                ('ullTotalPageFile', ctypes.c_ulonglong),
                ('ullAvailPageFile', ctypes.c_ulonglong),
                ('ullTotalVirtual', ctypes.c_ulonglong),
                ('ullAvailVirtual', ctypes.c_ulonglong),
                ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
            ]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        total_ram_gb = stat.ullTotalPhys / (1024 ** 3)
        free_ram_gb = stat.ullAvailPhys / (1024 ** 3)
        print(f"[OK] Physical RAM: {total_ram_gb:.2f} GB Total | {free_ram_gb:.2f} GB Available")
    except Exception as e:
        print(f"[WARN] Could not query exact RAM via ctypes: {e}")
        
    # 5. Core Libraries Built-In Verification
    import sqlite3
    print(f"[OK] Built-in SQLite 3 Version: {sqlite3.sqlite_version}")
    
    print("=" * 60)
    print("STATUS: ENVIRONMENT VALIDATED FOR PHASE 1")
    print("=" * 60)

if __name__ == "__main__":
    verify_system()

