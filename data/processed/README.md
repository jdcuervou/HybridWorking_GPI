## Processed Data

Esta carpeta almacena los datos procesados y limpios, listos para análisis.

Los archivos procesados son generados por los scripts del pipeline y típicamente incluyen:

- Datos con valores faltantes imputados o removidos
- Variables transformadas o ingenierizadas
- Datasets unidos o filtrados según criterios de análisis
- Archivos en formatos optimizados (parquet, feather, etc.)

### Generación

Los datos procesados se generan ejecutando:
```bash
python scripts/02_process_data.py
```

### Política de versionado

Los archivos procesados pueden versionarse si son livianos (< 10 MB) y 
facilitan la reproducibilidad. Archivos más grandes deben agregarse al 
`.gitignore` y regenerarse localmente.
