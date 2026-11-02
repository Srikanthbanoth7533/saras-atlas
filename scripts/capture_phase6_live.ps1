# SARAS ATLAS — Live Browser Screenshot Verification Script
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$outDirDesktop = "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\docs\screenshots\phase6_live\desktop"
$outDirLaptop = "C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\docs\screenshots\phase6_live\laptop"
$brainDir = "C:\Users\DELL\.gemini\antigravity\brain\5f10c8a8-c50f-4079-8a19-3fd3e3935301\screenshots\phase6_live"

New-Item -ItemType Directory -Force -Path $outDirDesktop | Out-Null
New-Item -ItemType Directory -Force -Path $outDirLaptop | Out-Null
New-Item -ItemType Directory -Force -Path $brainDir | Out-Null

$tabs = @(
    @{ Id = "situation_room"; Name = "01_situation_room.png" },
    @{ Id = "digital_twin"; Name = "02_digital_twin_topology.png" },
    @{ Id = "risks"; Name = "03_risk_sentinels.png" },
    @{ Id = "simulation"; Name = "04_simulation_studio.png" },
    @{ Id = "comparison"; Name = "05_scenario_comparison.png" },
    @{ Id = "optimization"; Name = "06_prescriptive_optimization.png" },
    @{ Id = "batch"; Name = "07_batch_scenario_engine.png" },
    @{ Id = "policy"; Name = "08_dynamic_policy_optimization.png" },
    @{ Id = "ingestion"; Name = "09_data_ingestion_center.png" },
    @{ Id = "intelligence"; Name = "10_ai_copilot_intelligence.png" },
    @{ Id = "rca"; Name = "11_root_cause_analysis.png" },
    @{ Id = "forecasting"; Name = "12_forecasting_studio.png" },
    @{ Id = "reports"; Name = "13_executive_reporting.png" },
    @{ Id = "connectors"; Name = "14_cloud_connectors.png" },
    @{ Id = "waterfall"; Name = "15_financial_waterfall.png" },
    @{ Id = "governance"; Name = "16_governance_audit.png" }
)

Write-Host "Capturing desktop screenshots (1440x960)..."
foreach ($t in $tabs) {
    $url = "http://localhost:3000/?tab=$($t.Id)"
    $dest = Join-Path $outDirDesktop $t.Name
    $bDest = Join-Path $brainDir $t.Name
    Write-Host "  Capturing $($t.Id)..."
    Start-Process -FilePath $edgePath -ArgumentList "--headless=new", "--disable-gpu", "--window-size=1440,960", "--virtual-time-budget=6000", "--screenshot=""$dest""", "$url" -Wait
    Start-Sleep -Milliseconds 500
    if (Test-Path $dest) {
        $size = (Get-Item $dest).Length
        Copy-Item -Path $dest -Destination $bDest -Force
        Write-Host "    [OK] $($t.Name) ($size bytes)"
    } else {
        Write-Host "    [FAIL] $($t.Name) missing"
    }
}

Write-Host "`nCapturing compact viewport screenshots (1024x768)..."
foreach ($t in $tabs[0..3]) {
    $url = "http://localhost:3000/?tab=$($t.Id)"
    $dest = Join-Path $outDirLaptop ("laptop_" + $t.Name)
    Write-Host "  Capturing compact $($t.Id)..."
    Start-Process -FilePath $edgePath -ArgumentList "--headless=new", "--disable-gpu", "--window-size=1024,768", "--virtual-time-budget=5000", "--screenshot=""$dest""", "$url" -Wait
    Start-Sleep -Milliseconds 500
    if (Test-Path $dest) {
        $size = (Get-Item $dest).Length
        Write-Host "    [OK] laptop_$($t.Name) ($size bytes)"
    }
}

Write-Host "`nAll screenshot captures complete!"

