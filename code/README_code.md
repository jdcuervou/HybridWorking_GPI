## Code (DEPRECADA)

⚠️ **Esta carpeta está deprecada desde la reorganización del proyecto.**

### Nueva estructura

El código del proyecto ahora se organiza en:

- **`scripts/`**: Scripts numerados del pipeline (ej: `01_download_data.py`)
- **`src/`**: Módulos de código reutilizable (ej: `config.py`, `utilidades.py`)

### Migración

Los archivos de esta carpeta han sido migrados:

- `download_data_from_doi.py` → **`scripts/01_download_data.py`**
- `requirements.txt` → **`environment.yml`** (gestión con conda)

### Instalación actual

```bash
# Crear entorno conda
conda env create -f environment.yml
conda activate hybridworking-gpi

# Ejecutar pipeline
./runall.ps1  # Windows
./runall.sh   # Linux/Mac
```

Ver [README.md](../README.md) principal para la documentación actualizada.
