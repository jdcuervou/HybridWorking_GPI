# PowerShell script to execute the full pipeline
# Project: HybridWorking_GPI
# Replication of Bloom et al. (2024)

Write-Host "`n======================================================================"
Write-Host "FULL PIPELINE - BLOOM ET AL. (2024) REPLICATION"
Write-Host "Hybrid working from home improves retention without damaging performance"
Write-Host "======================================================================`n"

# Configure PYTHONPATH
$env:PYTHONPATH = $PWD
$pythonExe = Join-Path $PWD ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "`nERROR: Python executable not found at $pythonExe" -ForegroundColor Red
    exit 1
}

# 1. Download data from DOI
Write-Host "STEP 1/2: Downloading data from Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
Write-Host "----------------------------------------------------------------------"
& $pythonExe scripts/01_download_data_clean.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Data download failed" -ForegroundColor Red
    exit 1
}

# 2. Generate figure 2
Write-Host "`nSTEP 2/2: Generating Figure 2 replica..."
Write-Host "----------------------------------------------------------------------"
& $pythonExe scripts/02_generate_figure.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Figure generation failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================================================"
Write-Host "Pipeline complete" -ForegroundColor Green
Write-Host "Data saved in: data/raw/" -ForegroundColor Cyan
Write-Host "Figure saved in: results/figures/figure2_replica.png" -ForegroundColor Cyan
Write-Host "Table saved in: results/tables/figure2_summary.csv" -ForegroundColor Cyan
Write-Host "======================================================================`n"
