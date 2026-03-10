## Raw data

Carpeta para datos originales descargados desde Harvard Dataverse.

- Fuente: Bloom, N., Han, R., & Liang, J. (2024)
- DOI dataset: `10.7910/DVN/6X4ZZL`

## Descarga

```bash
python scripts/01_download_data_clean.py
```

Comportamiento por defecto del script:
- Filtra por `figure2`.
- Descarga desde Dataverse.
- Convierte `.tab/.tsv` a `.csv`.
- Guarda en esta carpeta (`data/raw/`).

Ejemplo para descargar todo el dataset:

```bash
python scripts/01_download_data_clean.py --filter ""
```

## Archivo clave en esta replica
- `figure2.csv`: insumo principal para reproducir Figura 2.

## Versionado
Versionar solo archivos necesarios para reproducibilidad del ejercicio.
Si se descargan archivos grandes adicionales, preferir regenerarlos localmente.
