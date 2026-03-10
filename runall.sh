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
echo "PASO 1/3: Descargando datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)..."
echo "----------------------------------------------------------------------"
python scripts/01_download_data_clean.py

# 2. Generar figura 2
echo ""
echo "PASO 2/3: Generando réplica de Figura 2..."
echo "----------------------------------------------------------------------"
python scripts/02_generate_figure.py

# 3. Validar replica
echo ""
echo "PASO 3/3: Validando resultados de la replica..."
echo "----------------------------------------------------------------------"
python scripts/03_validate_replication.py

echo ""
echo "======================================================================"
echo "Pipeline completo ✅"
echo "Datos guardados en: data/raw/"
echo "Figura guardada en: results/figures/figure2_replica.png"
echo "Tabla guardada en: results/tables/figure2_summary.csv"
echo "Validacion guardada en: results/tables/validation_comparison.csv"
echo "Grafico de validacion guardado en: results/figures/validation_discrepancies.png"
echo "Tabla (imagen) guardada en: results/figures/validation_table_journal.png"
echo "======================================================================"
echo ""
