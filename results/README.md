## Resultados

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
python scripts/02_generate_figure.py
```

### Política de versionado

- **Versionar**: Figuras finales para publicación, tablas clave
- **No versionar**: Archivos intermedios voluminosos, salidas exploratorias extensas

Revisar `.gitignore` para detalles sobre qué se incluye en el repositorio.
