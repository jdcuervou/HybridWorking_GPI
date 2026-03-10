# HybridWorking_GPI
# Replicación: Hybrid working from home improves retention without damaging performance

## Paper seleccionado
Bloom, N., Han, R., & Liang, J. (2024).  
*Hybrid working from home improves retention without damaging performance*.  
Nature, 630(8018), 920–925.  
https://doi.org/10.1038/s41586-024-07500-2

## Integrantes del equipo
- Harold Acuña – Data Scientist
- Natalia Cortés - Data Engenier
- Jose D Cuervo – PMO

## Descripción del proyecto
Este proyecto busca reproducir parcialmente los resultados empíricos del artículo de Bloom et al. (2024),
que analiza el impacto del trabajo híbrido desde casa sobre la retención laboral y el desempeño de los trabajadores.

Siguiendo los lineamientos del curso, el equipo reproducirá un resultado específico basado en evidencia
cuantitativa reportada en el artículo, utilizando los datos y el código provistos por los autores en los
materiales suplementarios.

## Resultado a reproducir
Como ejercicio inicial, se planea reproducir el efecto del esquema de trabajo híbrido sobre la tasa de
retención de los empleados, uno de los principales hallazgos del artículo.

## Estructura del repositorio
```
HybridWorking_GPI/
├── data/
│   ├── raw/              # Datos originales descargados
│   └── processed/        # Datos procesados para análisis
├── scripts/              # Scripts numerados del pipeline
│   └── 01_download_data.py
├── src/                  # Módulos de código reutilizable
│   ├── __init__.py
│   └── config.py
├── results/              # Resultados generados
│   ├── figures/          # Gráficos y visualizaciones
│   └── tables/           # Tablas de resultados
├── docs/                 # Documentación del proyecto
├── environment.yml       # Dependencias conda
├── runall.ps1           # Pipeline completo (Windows)
└── runall.sh            # Pipeline completo (Linux/Mac)
```

Cada carpeta contiene un archivo README que describe su contenido.

## Requisitos técnicos
- **Lenguaje**: Python 3.11+
- **Gestor de entornos**: Conda
- **Paquetes principales**: pandas, numpy, statsmodels, scikit-learn, matplotlib, seaborn

## Instalación y uso

### 1. Crear entorno conda
```bash
conda env create -f environment.yml
conda activate hybridworking-gpi
```

### 2. Ejecutar pipeline completo

**Windows (PowerShell):**
```powershell
.\runall.ps1
```

**Linux/Mac:**
```bash
chmod +x runall.sh
./runall.sh
```

### 3. Ejecutar scripts individuales
```bash
python scripts/01_download_data.py
```

## Troubleshooting

Si encuentras problemas al ejecutar el pipeline, consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para diagnóstico detallado y soluciones comunes.

## Estado del proyecto
Este repositorio corresponde al Avance 1 del Proyecto Transversal del curso
Gestión de Proyectos de Investigación y Ciencia Abierta.
