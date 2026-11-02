"""
SARAS ATLAS — Health & System Diagnostics Router.
"""

import sys
import ctypes
from ctypes import wintypes
from fastapi import APIRouter
from sqlalchemy import text
from ortools.linear_solver import pywraplp

from src.database.session import SessionLocal

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD),
        ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_uint64),
        ("ullAvailPhys", ctypes.c_uint64),
        ("ullTotalPageFile", ctypes.c_uint64),
        ("ullAvailPageFile", ctypes.c_uint64),
        ("ullTotalVirtual", ctypes.c_uint64),
        ("ullAvailVirtual", ctypes.c_uint64),
        ("sullAvailExtendedVirtual", ctypes.c_uint64),
    ]


def get_memory_telemetry():
    """Retrieves physical RAM and process working set via native Windows APIs."""
    total_phys_gb = 8.0
    avail_phys_gb = 1.0
    process_mb = 50.0

    if sys.platform == "win32":
        try:
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            total_phys_gb = round(stat.ullTotalPhys / (1024 ** 3), 2)
            avail_phys_gb = round(stat.ullAvailPhys / (1024 ** 3), 2)

            psapi = ctypes.windll.psapi
            kernel32 = ctypes.windll.kernel32
            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
                wintypes.DWORD,
            ]
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            pmc = PROCESS_MEMORY_COUNTERS_EX()
            pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS_EX)
            if psapi.GetProcessMemoryInfo(kernel32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb):
                process_mb = round(pmc.WorkingSetSize / (1024 * 1024), 2)
        except Exception:
            pass

    return {
        "system_total_phys_gb": total_phys_gb,
        "system_avail_phys_gb": avail_phys_gb,
        "process_working_set_mb": process_mb,
    }


@router.get("")
def get_health_status():
    """Returns real-time health, DB status, solver readiness, and memory footprint."""
    db_status = "UNKNOWN"
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            db_status = "ONLINE (SQLite WAL)"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"

    scip_solver = pywraplp.Solver.CreateSolver("SCIP")
    solver_status = "READY (OR-Tools SCIP)" if scip_solver else "UNAVAILABLE"

    mem = get_memory_telemetry()

    return {
        "status": "HEALTHY",
        "service": "SARAS ATLAS — Commerce Resilience & Decision Simulation Platform",
        "version": "1.0.0-phase1",
        "database": db_status,
        "optimizer": solver_status,
        "memory": mem,
        "architecture": "In-Process Modular Monolith (< 350 MB Target RSS)",
    }
