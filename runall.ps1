# Script de PowerShell para ejecutar el pipeline completo
# Proyecto: HybridWorking_GPI
# Replicacion de Bloom et al. (2024)

Write-Host "`n======================================================================"
Write-Host "PIPELINE COMPLETO - REPLICACION BLOOM ET AL. (2024)"
Write-Host "Hybrid working from home improves retention without damaging performance"
Write-Host "======================================================================`n"

# Configurar PYTHONPATH
$env:PYTHONPATH = $PWD
$pythonExe = Join-Path $PWD ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "`nERROR: No se encontro el ejecutable de Python en $pythonExe" -ForegroundColor Red
    exit 1
}

# 1. Descargar datos desde DOI
Write-Host "PASO 1/3: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
Write-Host "----------------------------------------------------------------------"
& $pythonExe scripts/01_download_data_clean.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Fallo en la descarga de datos" -ForegroundColor Red
    exit 1
}

# 2. Generar figura 2
Write-Host "`nPASO 2/3: Generando replica de Figura 2..."
Write-Host "----------------------------------------------------------------------"
& $pythonExe scripts/02_generate_figure.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Fallo en la generacion de figura" -ForegroundColor Red
    exit 1
}

# 3. Validar replica
Write-Host "`nPASO 3/3: Validando resultados de la replica..."
Write-Host "----------------------------------------------------------------------"
& $pythonExe scripts/03_validate_replication.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Fallo en la validacion de resultados" -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================================================"
Write-Host "Pipeline completo" -ForegroundColor Green
Write-Host "Datos guardados en: data/raw/" -ForegroundColor Cyan
Write-Host "Figura guardada en: results/figures/figure2_replica.png" -ForegroundColor Cyan
Write-Host "Tabla guardada en: results/tables/figure2_summary.csv" -ForegroundColor Cyan
Write-Host "Validacion guardada en: results/tables/validation_comparison.csv" -ForegroundColor Cyan
Write-Host "Grafico de validacion guardado en: results/figures/validation_discrepancies.png" -ForegroundColor Cyan
Write-Host "Tabla (imagen) guardada en: results/figures/validation_table_journal.png" -ForegroundColor Cyan
Write-Host "======================================================================`n"
