## Results

Esta carpeta contiene todos los resultados generados por el pipeline de análisis.

### Estructura

- **figures/**: Gráficos, visualizaciones y figuras para reportes
- **tables/**: Tablas de resultados, coeficientes, métricas de modelos

### Generación

Los resultados se generan ejecutando el pipeline completo o scripts específicos:

```bash
# Pipeline completo
./runall.ps1  # Windows
./runall.sh   # Linux/Mac

# Scripts individuales
python scripts/03_analyze.py
python scripts/04_visualize.py
```

### Política de versionado

- **Versionar**: Figuras finales para publicación, tablas clave
- **No versionar**: Archivos intermedios voluminosos, salidas exploratorias extensas

Revisar `.gitignore` para detalles sobre qué se incluye en el repositorio.
