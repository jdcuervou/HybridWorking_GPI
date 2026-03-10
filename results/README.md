## Resultados

Esta carpeta centraliza las salidas generadas por el pipeline reproducible.

## Estructura
- `figures/`: figuras finales y graficos de validacion.
- `tables/`: tablas resumen y comparaciones paper vs replica.

## Archivos esperados

Al ejecutar el flujo completo deberian aparecer, al menos:

- `figures/figure2_replica.png`
- `figures/validation_discrepancies.png`
- `figures/validation_table_journal.png`
- `tables/figure2_summary.csv`
- `tables/validation_comparison.csv`

## Como generarlos

```bash
python scripts/01_download_data_clean.py
python scripts/02_generate_figure.py
python scripts/03_validate_replication.py
```

o con el pipeline completo:

- Windows: `./runall.ps1`
- Linux/Mac: `./runall.sh`

## Versionado
- Versionar resultados finales usados en el reporte.
- Evitar versionar salidas exploratorias o archivos grandes no esenciales.
- Revisar `.gitignore` para la politica vigente del repositorio.
