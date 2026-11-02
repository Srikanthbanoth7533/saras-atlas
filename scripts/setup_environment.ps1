# SARAS ATLAS — Automated Environment Setup Script
$ErrorActionPreference = 'Stop'

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SARAS ATLAS -- AUTOMATED ENVIRONMENT SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Project Directory Verification
$ProjectRoot = "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas"
if (-not (Test-Path $ProjectRoot)) {
    Write-Host "FAILED: Project directory does not exist: $ProjectRoot" -ForegroundColor Red
    exit 1
}
Set-Location $ProjectRoot
Write-Host "SUCCESS: Project Root: $ProjectRoot" -ForegroundColor Green

# 2. Python 3.12 Discovery
$Python312Path = "C:\Users\DELL\AppData\Local\Python\pythoncore-3.12-64\python.exe"
if (-not (Test-Path $Python312Path)) {
    Write-Host "WARNING: Specific Python 3.12 path not found. Checking system..." -ForegroundColor Yellow
}

if (-not (Test-Path $Python312Path)) {
    Write-Host "FAILED: Python 3.12 is required but could not be located." -ForegroundColor Red
    exit 1
}
Write-Host "SUCCESS: Using Python 3.12: $Python312Path" -ForegroundColor Green

# 3. Virtual Environment Creation
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "INFO: Creating isolated virtual environment in .venv..." -ForegroundColor Yellow
    & $Python312Path -m venv $VenvDir
    Write-Host "SUCCESS: Virtual environment created successfully." -ForegroundColor Green
} else {
    Write-Host "SUCCESS: Existing virtual environment detected." -ForegroundColor Green
}

# 4. Pip & Setup Verification
Write-Host "INFO: Verifying virtual environment pip..." -ForegroundColor Yellow
& $VenvPython -m pip --version

# 5. Execute Verification
Write-Host "INFO: Running verify_environment.py..." -ForegroundColor Yellow
& $VenvPython (Join-Path $ProjectRoot "scripts\verify_environment.py")

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE: SARAS ATLAS READY FOR PHASE 1" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
