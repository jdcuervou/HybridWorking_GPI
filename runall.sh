#!/usr/bin/env bash
set -e

# Script Bash para ejecutar el pipeline completo
# Proyecto: HybridWorking_GPI
# Replicación de Bloom et al. (2024)

echo ""
echo "======================================================================"
echo "PIPELINE COMPLETO - REPLICACIÓN BLOOM ET AL. (2024)"
echo "Hybrid working from home improves retention without damaging performance"
echo "======================================================================" 
echo ""

# Moverse a la carpeta raíz del proyecto
cd "$(dirname "$0")"

# Asegurar que el proyecto esté en el PYTHONPATH
export PYTHONPATH="$(pwd)"

# 1. Descargar datos desde DOI
echo "PASO 1/1: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
echo "----------------------------------------------------------------------"
python scripts/01_download_data.py

echo ""
echo "======================================================================"
echo "Pipeline de descarga completo ✅"
echo "Datos guardados en: data/raw/"
echo "======================================================================"
echo ""
echo "Próximos pasos sugeridos:"
echo "  - Revisar los datos descargados en data/raw/"
echo "  - Crear scripts 02_process_data.py y 03_analyze.py"
echo "  - Agregar nuevas etapas al pipeline según avance el proyecto"
echo ""
