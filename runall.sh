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
echo "PASO 1/2: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
echo "----------------------------------------------------------------------"
python scripts/01_download_data_clean.py

# 2. Generar figura 2
echo ""
echo "PASO 2/2: Generando réplica de Figura 2..."
echo "----------------------------------------------------------------------"
python scripts/02_generate_figure.py

echo ""
echo "======================================================================"
echo "Pipeline completo ✅"
echo "Datos guardados en: data/raw/"
echo "Figura guardada en: results/figures/figure2_replica.png"
echo "Tabla guardada en: results/tables/figure2_summary.csv"
echo "======================================================================"
echo ""
