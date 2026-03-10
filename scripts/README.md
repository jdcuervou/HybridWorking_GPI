## Scripts

Esta carpeta contiene los scripts numerados que conforman el pipeline de análisis,
diseñados para ejecutarse de forma secuencial.

### Scripts disponibles

- **01_download_data_clean.py**: Descarga automática de datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)
  - Por defecto, filtra y descarga solo el archivo de la Figura 2
  - Convierte archivos .tab a formato CSV
  - Guarda directamente en `data/raw/`

- **02_generate_figure.py**: Genera la réplica de la Figura 2 del paper
  - Lee datos desde `data/raw/figure2.csv`
  - Genera gráficos comparando attrition entre grupos
  - Guarda figura en `results/figures/figure2_replica.png`
  - Guarda tabla resumen en `results/tables/figure2_summary.csv`

### Uso individual

```bash
# Desde la raíz del proyecto
python scripts/01_download_data_clean.py
python scripts/02_generate_figure.py

# Con parámetros opcionales para descarga
python scripts/01_download_data_clean.py --doi 10.7910/DVN/6X4ZZL --filter figure2 --output-dir data/raw

# Descargar todos los archivos (sin filtro)
python scripts/01_download_data_clean.py --filter ""
```

**Parámetros disponibles:**
- `--doi`: DOI del dataset (por defecto: 10.7910/DVN/6X4ZZL)
- `--filter`: Filtrar archivos por nombre (por defecto: "figure2")
- `--output-dir`: Directorio de salida (por defecto: data/raw/)

### Próximos scripts planeados

- **03_robustness_checks.py**: Análisis de robustez y sensibilidad
- **04_extended_analysis.py**: Análisis exploratorio extendido

### Ejecución del pipeline completo

Ver scripts `runall.ps1` (Windows) o `runall.sh` (Linux/Mac) en la raíz del proyecto.
