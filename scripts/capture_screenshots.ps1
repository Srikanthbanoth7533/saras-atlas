# SARAS ATLAS — Automated Screenshot Capture Script
# Starts FastAPI backend + Next.js frontend, captures 8 high-resolution screenshots via headless Edge, and cleans up.

$ErrorActionPreference = "SilentlyContinue"

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    Write-Host "Edge binary not found at $edgePath"
    exit 1
}

$outputDir = "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\docs\screenshots"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

$brainDir = "C:\Users\DELL\.gemini\antigravity\brain\5f10c8a8-c50f-4079-8a19-3fd3e3935301\screenshots"
if (-not (Test-Path $brainDir)) {
    New-Item -ItemType Directory -Force -Path $brainDir | Out-Null
}

Write-Host "[1/4] Starting FastAPI backend on port 8000..."
$backendProcess = Start-Process -FilePath "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\.venv\Scripts\python.exe" `
    -ArgumentList "-m", "uvicorn", "src.api.main:app", "--host", "127.0.0.1", "--port", "8000" `
    -WorkingDirectory "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas" `
    -PassThru

Write-Host "[2/4] Starting Next.js frontend on port 3000..."
$frontendProcess = Start-Process -FilePath "npm.cmd" `
    -ArgumentList "run", "start" `
    -WorkingDirectory "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\frontend" `
    -PassThru

# Wait for servers to be live
Start-Sleep -Seconds 6

$tabs = @(
    @{ Name = "01_situation_room.png"; Url = "http://localhost:3000/?tab=situation_room" },
    @{ Name = "02_digital_twin_topology.png"; Url = "http://localhost:3000/?tab=digital_twin" },
    @{ Name = "03_risk_sentinels.png"; Url = "http://localhost:3000/?tab=risks" },
    @{ Name = "04_simulation_studio.png"; Url = "http://localhost:3000/?tab=simulation" },
    @{ Name = "05_scenario_comparison.png"; Url = "http://localhost:3000/?tab=comparison" },
    @{ Name = "06_prescriptive_optimization.png"; Url = "http://localhost:3000/?tab=optimization" },
    @{ Name = "07_financial_waterfall.png"; Url = "http://localhost:3000/?tab=waterfall" },
    @{ Name = "08_governance_two_man_rule.png"; Url = "http://localhost:3000/?tab=governance" },
    @{ Name = "09_batch_scenario_engine.png"; Url = "http://localhost:3000/?tab=batch" },
    @{ Name = "10_dynamic_policy_optimization.png"; Url = "http://localhost:3000/?tab=policy" },
    @{ Name = "11_enterprise_data_ingestion.png"; Url = "http://localhost:3000/?tab=ingestion" },
    @{ Name = "12_intelligence_center.png"; Url = "http://localhost:3000/?tab=intelligence" },
    @{ Name = "13_root_cause_analysis.png"; Url = "http://localhost:3000/?tab=rca" },
    @{ Name = "14_forecasting_studio.png"; Url = "http://localhost:3000/?tab=forecasting" },
    @{ Name = "15_executive_reporting.png"; Url = "http://localhost:3000/?tab=reports" },
    @{ Name = "16_enterprise_connectors.png"; Url = "http://localhost:3000/?tab=connectors" }
)

Write-Host "[3/4] Capturing interface screenshots via headless Microsoft Edge..."
foreach ($tab in $tabs) {
    $outFile = Join-Path $outputDir $tab.Name
    $brainFile = Join-Path $brainDir $tab.Name
    Write-Host "  Capturing $($tab.Name)..."
    
    Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--window-size=1440,960", "--virtual-time-budget=5000", "--screenshot=""$outFile""", "$($tab.Url)" -Wait
    Start-Sleep -Seconds 1
    if (Test-Path $outFile) {
        Copy-Item -Path $outFile -Destination $brainFile -Force
        Write-Host "    [OK] Captured $outFile"
    } else {
        Write-Host "    [FAIL] Could not capture $outFile"
    }
}

Write-Host "[4/4] Tearing down temporary background processes..."
if ($backendProcess) {
    Stop-Process -Id $backendProcess.Id -Force
}
if ($frontendProcess) {
    Stop-Process -Id $frontendProcess.Id -Force
}

# Cleanup any orphan node/python listeners on 3000 and 8000
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

Write-Host "Screenshot capture complete!"

