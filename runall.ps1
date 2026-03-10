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
Write-Host "PASO 1/1: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
Write-Host "----------------------------------------------------------------------"
python scripts/01_download_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ ERROR: Fallo en la descarga de datos" -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================================================"
Write-Host "Pipeline de descarga completo ✅" -ForegroundColor Green
Write-Host "Datos guardados en: data/raw/" -ForegroundColor Cyan
Write-Host "======================================================================`n"
Write-Host "Próximos pasos sugeridos:" -ForegroundColor Yellow
Write-Host "  - Revisar los datos descargados en data/raw/"
Write-Host "  - Crear scripts 02_process_data.py y 03_analyze.py"
Write-Host "  - Agregar nuevas etapas al pipeline según avance el proyecto`n"
