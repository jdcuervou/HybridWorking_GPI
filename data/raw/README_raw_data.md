## Raw Data

Esta carpeta contiene los datos originales descargados automáticamente
desde Harvard Dataverse.

**Fuente**: Bloom, N., Han, R., & Liang, J. (2024)  
**DOI**: 10.7910/DVN/6X4ZZL  
**URL**: https://doi.org/10.1038/s41586-024-07500-2

### Descarga automática

Los datos se descargan ejecutando:
```bash
python scripts/01_download_data_clean.py
```

El script:
- Descarga automáticamente el archivo de la **Figura 2** del paper
- Convierte el formato .tab a CSV legible
- Guarda como `figure2.csv` en esta carpeta

Para descargar todos los archivos del dataset:
```bash
python scripts/01_download_data_clean.py --filter ""
```

### Política de versionado

Los datos raw **no se versionan** en este repositorio por su tamaño y 
disponibilidad pública. Cada colaborador debe descargarlos localmente 
usando el script provisto.
