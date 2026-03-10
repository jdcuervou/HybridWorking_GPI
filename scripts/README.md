## Scripts del pipeline

Esta carpeta contiene el flujo principal de replicacion, diseñado para ejecutarse en orden.

## Orden de ejecucion
1. `01_download_data_clean.py`
2. `02_generate_figure.py`
3. `03_validate_replication.py`

## Descripcion por script

### `01_download_data_clean.py`
Descarga datos desde Dataverse usando DOI.

- DOI por defecto: `10.7910/DVN/6X4ZZL`
- Filtro por defecto: `figure2`
- Convierte `.tab/.tsv` a `.csv`
- Salida por defecto: `data/raw/`

Parametros utiles:
- `--doi`: DOI del dataset
- `--filter`: Patron de nombre para filtrar archivos
- `--output-dir`: Carpeta de salida
- `--convert-csv`: bandera para conversion a CSV (habilitada por defecto en el script)

### `02_generate_figure.py`
Genera la replica de la Figura 2 a partir de `data/raw/figure2.csv`.

Salidas:
- `results/figures/figure2_replica.png`
- `results/tables/figure2_summary.csv`

Nota:
- Si `attrite_perc` viene en escala 0-100, el script lo normaliza a 0-1 antes de validar y calcular resultados.

### `03_validate_replication.py`
Compara la replica contra los valores del paper.

Salidas:
- `results/tables/validation_comparison.csv`
- `results/figures/validation_discrepancies.png`
- `results/figures/validation_table_journal.png`

## Uso

Desde la raiz del proyecto:

```bash
python scripts/01_download_data_clean.py
python scripts/02_generate_figure.py
python scripts/03_validate_replication.py
```

Ejemplos para descarga:

```bash
# Cambiar DOI/filtro/salida
python scripts/01_download_data_clean.py --doi 10.7910/DVN/6X4ZZL --filter figure2 --output-dir data/raw

# Descargar todos los archivos del dataset
python scripts/01_download_data_clean.py --filter ""
```

## Pipeline completo
Para ejecucion automatica de todos los pasos, usar:
- `runall.ps1` en Windows
- `runall.sh` en Linux/Mac
