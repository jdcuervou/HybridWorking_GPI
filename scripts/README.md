## Scripts

Esta carpeta contiene los scripts numerados que conforman el pipeline de análisis,
diseñados para ejecutarse de forma secuencial.

### Scripts disponibles

- **01_download_data.py**: Descarga automática de datos desde Harvard Dataverse (DOI: 10.7910/DVN/6X4ZZL)
  - Por defecto, filtra y descarga solo el archivo de la Figura 2
  - Convierte archivos .tab a formato CSV
  - Guarda directamente en `data/raw/`

### Uso individual

```bash
# Desde la raíz del proyecto
python scripts/01_download_data.py

# Con parámetros opcionales
python scripts/01_download_data.py --filter figure2 --convert-csv

# Descargar todos los archivos (sin filtro)
python scripts/01_download_data.py --filter ""
```

**Parámetros disponibles:**
- `--doi`: DOI del dataset (por defecto: 10.7910/DVN/6X4ZZL)
- `--filter`: Filtrar archivos por nombre (por defecto: "figure2")
- `--convert-csv`: Convertir .tab a CSV (por defecto: True)
- `--output-dir`: Directorio de salida (por defecto: data/raw/)

### Próximos scripts planeados

- **02_process_data.py**: Limpieza y procesamiento de datos
- **03_analyze.py**: Análisis estadístico y modelado
- **04_visualize.py**: Generación de figuras y tablas

### Ejecución del pipeline completo

Ver scripts `runall.ps1` (Windows) o `runall.sh` (Linux/Mac) en la raíz del proyecto.
