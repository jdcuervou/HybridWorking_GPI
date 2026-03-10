## Processed Data

Esta carpeta almacena los datos procesados y limpios, listos para análisis.

Los archivos procesados son generados por los scripts del pipeline y típicamente incluyen:

- Datos con valores faltantes imputados o removidos
- Variables transformadas o ingenierizadas
- Datasets unidos o filtrados según criterios de análisis
- Archivos en formatos optimizados (parquet, feather, etc.)

### Generación

En el estado actual del proyecto no hay un script dedicado de procesamiento en `scripts/`.
Los resultados reproducidos se generan directamente desde datos raw ejecutando:
```bash
python scripts/02_generate_figure.py
```

Si en etapas futuras se agrega un script de procesamiento, este README debe actualizarse.

### Política de versionado

Los archivos procesados pueden versionarse si son livianos (< 10 MB) y 
facilitan la reproducibilidad. Archivos más grandes deben agregarse al 
`.gitignore` y regenerarse localmente.
