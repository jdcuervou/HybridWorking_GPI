# Script de PowerShell para ejecutar el pipeline completo
# Proyecto: HybridWorking_GPI
# Replicación de Bloom et al. (2024)

Write-Host "`n======================================================================"
Write-Host "PIPELINE COMPLETO - REPLICACIÓN BLOOM ET AL. (2024)"
Write-Host "Hybrid working from home improves retention without damaging performance"
Write-Host "======================================================================`n"

# Configurar PYTHONPATH
$env:PYTHONPATH = $PWD

# 1. Descargar datos desde DOI
Write-Host "PASO 1/2: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
Write-Host "----------------------------------------------------------------------"
python scripts/01_download_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ ERROR: Fallo en la descarga de datos" -ForegroundColor Red
    exit 1
}

# 2. Generar figura 2
Write-Host "`nPASO 2/2: Generando réplica de Figura 2..."
Write-Host "----------------------------------------------------------------------"
python scripts/02_generate_figure.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ ERROR: Fallo en la generación de figura" -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================================================"
Write-Host "Pipeline completo ✅" -ForegroundColor Green
Write-Host "Datos guardados en: data/raw/" -ForegroundColor Cyan
Write-Host "Figura guardada en: results/figures/figure2_replica.png" -ForegroundColor Cyan
Write-Host "Tabla guardada en: results/tables/figure2_summary.csv" -ForegroundColor Cyan
Write-Host "======================================================================`n"
