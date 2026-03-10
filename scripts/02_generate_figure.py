from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# Configurar backend de matplotlib para evitar problemas sin GUI
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI, perfecto para guardar archivos

# Importar configuración del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import DATA_RAW_DIR, RESULTS_FIGURES_DIR, RESULTS_TABLES_DIR


# =========================
# Configuración
# =========================

@dataclass(frozen=True)
class Config:
    input_file: Path = DATA_RAW_DIR / "figure2.csv"
    output_figure: Path = RESULTS_FIGURES_DIR / "figure2_replica.png"
    output_summary: Path = RESULTS_TABLES_DIR / "figure2_summary.csv"
    dpi: int = 300


# =========================
# Carga y validación
# =========================

REQUIRED_COLUMNS = ["treat", "role", "male", "live_far", "attrite_perc"]


def load_data(file_path: Path) -> pd.DataFrame:
    """Carga el archivo CSV."""
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    df = pd.read_csv(file_path)

    # Algunos archivos traen attrite_perc en escala 0-100; normalizamos a 0-1.
    if "attrite_perc" in df.columns:
        df["attrite_perc"] = pd.to_numeric(df["attrite_perc"], errors="coerce")
        non_null = df["attrite_perc"].dropna()
        if not non_null.empty and float(non_null.max()) > 1:
            print("Advertencia: 'attrite_perc' detectado en escala 0-100. Se convertirá a 0-1.")
            df["attrite_perc"] = df["attrite_perc"] / 100.0

    return df


def validate_data(df: pd.DataFrame) -> None:
    """Valida que las columnas necesarias existan y tengan formato esperado."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    # Columnas clave para el cálculo principal: no deben tener nulos.
    strict_non_null_cols = ["treat", "attrite_perc"]
    for col in strict_non_null_cols:
        if df[col].isna().any():
            raise ValueError(f"La columna '{col}' contiene valores nulos.")

    # En subgrupos puede haber faltantes; avisamos para transparencia.
    subgroup_cols = ["role", "male", "live_far"]
    for col in subgroup_cols:
        null_count = int(df[col].isna().sum())
        if null_count > 0:
            print(
                f"Advertencia: la columna '{col}' contiene {null_count} nulos. "
                "Las métricas por subgrupo se calcularán con casos disponibles."
            )

    # Verificación básica de variables binarias
    binary_cols = ["treat", "role", "male", "live_far", "attrite_perc"]
    for col in binary_cols:
        unique_vals = set(df[col].dropna().unique())
        if not unique_vals.issubset({0, 1}):
            raise ValueError(
                f"La columna '{col}' debe ser binaria (0/1). Valores encontrados: {sorted(unique_vals)}"
            )

    if len(df) != 1612:
        print(
            f"Advertencia: el paper usa 1,612 observaciones. "
            f"Tu archivo tiene {len(df)} filas."
        )


# =========================
# Preparación de datos
# =========================

def prepare_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega etiquetas legibles para facilitar tablas y gráficos."""
    out = df.copy()

    out["treat_label"] = out["treat"].map({
        0: "In-person (control)",
        1: "Hybrid WFH (treatment)"
    })
    out["role_label"] = out["role"].map({
        0: "Non-managers",
        1: "Managers"
    })
    out["gender_label"] = out["male"].map({
        0: "Women",
        1: "Men"
    })
    out["commute_label"] = out["live_far"].map({
        0: "Commute of 90 mins\nor less",
        1: "Commute longer than\n90 mins"
    })

    return out


# =========================
# Resúmenes estadísticos
# =========================

def attrition_rate(series: pd.Series) -> float:
    """Convierte la media de variable binaria en porcentaje."""
    return float(series.mean() * 100)


def compute_group_means(
    df: pd.DataFrame,
    group_col: str | None = None,
) -> pd.DataFrame:
    """
    Calcula tasas de attrition por tratamiento y opcionalmente por subgrupo.
    """
    if group_col is None:
        result = (
            df.groupby("treat", as_index=False)["attrite_perc"]
            .mean()
            .assign(attrition_pct=lambda x: x["attrite_perc"] * 100)
        )
        return result

    result = (
        df.groupby([group_col, "treat"], as_index=False)["attrite_perc"]
        .mean()
        .assign(attrition_pct=lambda x: x["attrite_perc"] * 100)
    )
    return result


def welch_ttest(
    df: pd.DataFrame,
    subgroup_filter: pd.Series | None = None,
) -> Dict[str, float]:
    """
    Ejecuta t-test de Welch entre control y tratamiento.
    Devuelve diferencia en puntos porcentuales: control - treatment.
    """
    data = df.loc[subgroup_filter].copy() if subgroup_filter is not None else df.copy()

    control = data.loc[data["treat"] == 0, "attrite_perc"]
    treat = data.loc[data["treat"] == 1, "attrite_perc"]

    t_stat, p_value = stats.ttest_ind(control, treat, equal_var=False)
    diff_pp = (control.mean() - treat.mean()) * 100

    return {
        "n_control": int(control.shape[0]),
        "n_treat": int(treat.shape[0]),
        "control_mean_pct": float(control.mean() * 100),
        "treat_mean_pct": float(treat.mean() * 100),
        "difference_pp": float(diff_pp),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
    }


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Construye una tabla resumen con los paneles de la figura."""
    rows: List[Dict[str, object]] = []

    # Panel 1: total
    total_stats = welch_ttest(df)
    rows.append({
        "panel": "All employees",
        "subgroup": "All employees",
        **total_stats,
    })

    # Panel 2: role
    for role_value, role_name in [(0, "Non-managers"), (1, "Managers")]:
        stats_dict = welch_ttest(df, df["role"] == role_value)
        rows.append({
            "panel": "Role",
            "subgroup": role_name,
            **stats_dict,
        })

    # Panel 3: gender
    for male_value, gender_name in [(0, "Women"), (1, "Men")]:
        stats_dict = welch_ttest(df, df["male"] == male_value)
        rows.append({
            "panel": "Gender",
            "subgroup": gender_name,
            **stats_dict,
        })

    # Panel 4: commute
    for far_value, commute_name in [
        (0, "Commute of 90 mins or less"),
        (1, "Commute longer than 90 mins"),
    ]:
        stats_dict = welch_ttest(df, df["live_far"] == far_value)
        rows.append({
            "panel": "Commute",
            "subgroup": commute_name,
            **stats_dict,
        })

    summary = pd.DataFrame(rows)
    return summary


# =========================
# Construcción de datos para plot
# =========================

def get_panel_values_overall(df: pd.DataFrame) -> Tuple[List[str], List[float], List[float]]:
    temp = compute_group_means(df).sort_values("treat")
    labels = ["All employees"]
    control_vals = [temp.loc[temp["treat"] == 0, "attrition_pct"].iloc[0]]
    treat_vals = [temp.loc[temp["treat"] == 1, "attrition_pct"].iloc[0]]
    return labels, control_vals, treat_vals


def get_panel_values_by_role(df: pd.DataFrame) -> Tuple[List[str], List[float], List[float]]:
    temp = compute_group_means(df, "role")
    pivot = temp.pivot(index="role", columns="treat", values="attrition_pct")
    labels = ["Non-managers", "Managers"]
    control_vals = [pivot.loc[0, 0], pivot.loc[1, 0]]
    treat_vals = [pivot.loc[0, 1], pivot.loc[1, 1]]
    return labels, control_vals, treat_vals


def get_panel_values_by_gender(df: pd.DataFrame) -> Tuple[List[str], List[float], List[float]]:
    temp = compute_group_means(df, "male")
    pivot = temp.pivot(index="male", columns="treat", values="attrition_pct")
    labels = ["Women", "Men"]
    control_vals = [pivot.loc[0, 0], pivot.loc[1, 0]]
    treat_vals = [pivot.loc[0, 1], pivot.loc[1, 1]]
    return labels, control_vals, treat_vals


def get_panel_values_by_commute(df: pd.DataFrame) -> Tuple[List[str], List[float], List[float]]:
    temp = compute_group_means(df, "live_far")
    pivot = temp.pivot(index="live_far", columns="treat", values="attrition_pct")
    labels = ["Commute of 90 mins\nor less", "Commute longer than\n90 mins"]
    control_vals = [pivot.loc[0, 0], pivot.loc[1, 0]]
    treat_vals = [pivot.loc[0, 1], pivot.loc[1, 1]]
    return labels, control_vals, treat_vals


# =========================
# Gráficos
# =========================

def annotate_bars(ax, x_positions: np.ndarray, values: List[float], shift: float) -> None:
    """Escribe el valor encima de cada barra."""
    for x, y in zip(x_positions + shift, values):
        ax.text(
            x,
            y + 0.2,
            f"{y:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def plot_panel(
    ax: plt.Axes,
    labels: List[str],
    control_vals: List[float],
    treat_vals: List[float],
    title: str | None = None,
    p_values: List[float] | None = None,
) -> None:
    """Dibuja un panel de barras comparando control y tratamiento."""
    x = np.arange(len(labels))
    width = 0.35

    ax.bar(x - width / 2, control_vals, width, label="In-person (control)")
    ax.bar(x + width / 2, treat_vals, width, label="Hybrid WFH (treatment)")

    annotate_bars(ax, x, control_vals, -width / 2)
    annotate_bars(ax, x, treat_vals, width / 2)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Attrition (%)")
    ax.set_ylim(0, max(control_vals + treat_vals) + 3)

    if title:
        ax.set_title(title, fontsize=11)

    if p_values is not None:
        for i, p_val in enumerate(p_values):
            top = max(control_vals[i], treat_vals[i])
            ax.text(
                x[i],
                top + 1.2,
                f"P = {p_val:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )


def create_figure(df: pd.DataFrame, output_file: Path, dpi: int = 300) -> None:
    """Genera la figura 2 en formato 2x2."""
    # Asegurar que el directorio de salida existe
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: all employees
    labels, control_vals, treat_vals = get_panel_values_overall(df)
    p_overall = [welch_ttest(df)["p_value"]]
    plot_panel(
        axes[0, 0],
        labels,
        control_vals,
        treat_vals,
        title=None,
        p_values=p_overall,
    )

    # Panel 2: role
    labels, control_vals, treat_vals = get_panel_values_by_role(df)
    p_role = [
        welch_ttest(df, df["role"] == 0)["p_value"],
        welch_ttest(df, df["role"] == 1)["p_value"],
    ]
    plot_panel(
        axes[0, 1],
        labels,
        control_vals,
        treat_vals,
        title=None,
        p_values=p_role,
    )

    # Panel 3: gender
    labels, control_vals, treat_vals = get_panel_values_by_gender(df)
    p_gender = [
        welch_ttest(df, df["male"] == 0)["p_value"],
        welch_ttest(df, df["male"] == 1)["p_value"],
    ]
    plot_panel(
        axes[1, 0],
        labels,
        control_vals,
        treat_vals,
        title=None,
        p_values=p_gender,
    )

    # Panel 4: commute
    labels, control_vals, treat_vals = get_panel_values_by_commute(df)
    p_commute = [
        welch_ttest(df, df["live_far"] == 0)["p_value"],
        welch_ttest(df, df["live_far"] == 1)["p_value"],
    ]
    plot_panel(
        axes[1, 1],
        labels,
        control_vals,
        treat_vals,
        title=None,
        p_values=p_commute,
    )

    handles, labels_legend = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels_legend, loc="upper center", ncol=2, frameon=False)

    fig.suptitle("Figure 2 Replica — Attrition rates", fontsize=14, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


# =========================
# Reporte en consola
# =========================

def print_main_results(summary: pd.DataFrame) -> None:
    """Imprime resultados principales en consola."""
    print("\n=== Resumen de Figure 2 ===")
    print(summary[[
        "panel",
        "subgroup",
        "control_mean_pct",
        "treat_mean_pct",
        "difference_pp",
        "p_value",
    ]].to_string(index=False))

    print("\nInterpretación:")
    print("- difference_pp = tasa control - tasa treatment")
    print("- Un valor positivo implica menor attrition bajo Hybrid WFH")


# =========================
# Main
# =========================

def main() -> None:
    try:
        config = Config()

        print(f"Leyendo datos desde: {config.input_file}")
        if not config.input_file.exists():
            raise FileNotFoundError(
                f"\n❌ No se encontró el archivo: {config.input_file}\n"
                f"Ejecuta primero: python scripts/01_download_data.py"
            )
        
        df = load_data(config.input_file)
        validate_data(df)
        df = prepare_labels(df)

        print(f"\nGenerando tabla resumen...")
        summary = build_summary_table(df)
        config.output_summary.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(config.output_summary, index=False)

        print(f"Generando figura...")
        create_figure(df, config.output_figure, dpi=config.dpi)
        print_main_results(summary)

        print(f"\n✅ Figura guardada en: {config.output_figure}")
        print(f"✅ Resumen guardado en: {config.output_summary}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"\nVer TROUBLESHOOTING.md para más ayuda")
        raise


if __name__ == "__main__":
    main()
