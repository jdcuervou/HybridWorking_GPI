# HybridWorking_GPI

Replicacion del paper *Hybrid working from home improves retention without damaging performance* (Bloom, Han y Liang, 2024).

## Referencia
- Articulo: Nature 630(8018), 920-925
- DOI paper: `10.1038/s41586-024-07500-2`
- DOI datos (Dataverse): `10.7910/DVN/6X4ZZL`

## Objetivo
Reproducir la Figura 2 del paper y validar la cercania entre los resultados reportados y la replica.

## Estructura
```text
HybridWorking_GPI/
|-- code/                    # Scripts auxiliares del proyecto
|-- data/
|   |-- raw/                 # Datos originales descargados (ej. figure2.csv)
|   `-- processed/           # Datos transformados/intermedios (si aplica)
|-- docs/                    # Notas y documentacion de apoyo
|-- results/
|   |-- figures/             # Figuras generadas
|   `-- tables/              # Tablas de resultados
|-- scripts/                 # Pipeline principal reproducible
|   |-- 01_download_data_clean.py
|   |-- 02_generate_figure.py
|   `-- 03_validate_replication.py
|-- src/
|   `-- config.py            # Configuracion central (rutas, DOI, etc.)
|-- environment.yml
|-- runall.ps1               # Pipeline completo en Windows
`-- runall.sh                # Pipeline completo en Linux/Mac
```

## Requisitos
- Python 3.11+
- Dependencias en `environment.yml` (Conda) o `code/requirements.txt` (pip)

## Instalacion

### Opcion A: Conda
```bash
conda env create -f environment.yml
conda activate hybridworking-gpi
```

### Opcion B: venv + pip
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install -r code/requirements.txt
```

## Ejecucion

### Pipeline completo
```powershell
# Windows
.\runall.ps1
```

```bash
# Linux/Mac
chmod +x runall.sh
./runall.sh
```

### Ejecucion paso a paso
```bash
python scripts/01_download_data_clean.py
python scripts/02_generate_figure.py
python scripts/03_validate_replication.py
```

## Salidas esperadas
- `c`
- `results/figures/figure2_replica.png`
- `results/tables/figure2_summary.csv`
- `results/tables/validation_comparison.csv`
- `results/figures/validation_discrepancies.png`
- `results/figures/validation_table_journal.png`

## Equipo
- Harold Acuna - Data Scientist
- Natalia Cortes - Data Engineer
- Jose D Cuervo - PMO

## Documentación y entregables
Contiene documentos en word de entrega 1 y entrega 2 para garantizar trazabilidad y documentación asociada a la entrega
```bash
- docs/Proyecto_Transversal.docs
- docs/Parte 3 Avance GPI.docs
```
