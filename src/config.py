"""
Módulo de configuración para el proyecto HybridWorking_GPI.

Define parámetros globales y rutas del proyecto para facilitar
la reproducibilidad y mantenimiento del código.
"""

from dataclasses import dataclass
from pathlib import Path


# Rutas base del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_FIGURES_DIR = RESULTS_DIR / "figures"
RESULTS_TABLES_DIR = RESULTS_DIR / "tables"


@dataclass(frozen=True)
class ProjectConfig:
    """
    Configuración inmutable para el proyecto de replicación.
    
    Attributes:
        doi (str): DOI del dataset principal del estudio original.
        seed (int): Semilla aleatoria para reproducibilidad.
        alpha (float): Nivel de significancia estadística.
    """
    
    doi: str = "10.7910/DVN/6X4ZZL"
    """DOI de Harvard Dataverse con los datos del estudio Bloom et al. (2024)"""
    
    seed: int = 42
    """Semilla para el generador de números aleatorios"""
    
    alpha: float = 0.05
    """Nivel de significancia estadística (5%)"""
