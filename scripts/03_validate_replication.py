from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Importar configuracion del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import RESULTS_FIGURES_DIR, RESULTS_TABLES_DIR


@dataclass(frozen=True)
class Config:
    input_summary: Path = RESULTS_TABLES_DIR / "figure2_summary.csv"
    output_comparison: Path = RESULTS_TABLES_DIR / "validation_comparison.csv"
    output_plot: Path = RESULTS_FIGURES_DIR / "validation_discrepancies.png"
    output_table_image: Path = RESULTS_FIGURES_DIR / "validation_table_journal.png"
    dpi: int = 300


def build_paper_reference() -> pd.DataFrame:
    """Resultados de referencia reportados en el paper."""
    return pd.DataFrame(
        {
            "panel_paper": [
                "All employees",
                "Non-managers",
                "Managers",
                "Women",
                "Men",
                "Commute short",
                "Commute long",
            ],
            "subgroup": [
                "All employees",
                "Non-managers",
                "Managers",
                "Women",
                "Men",
                "Commute of 90 mins or less",
                "Commute longer than 90 mins",
            ],
            "control_paper": [7.2, 8.6, 3.0, 9.2, 6.1, 7.7, 6.0],
            "treat_paper": [4.8, 5.3, 3.1, 4.2, 5.1, 5.1, 2.9],
        }
    )


def load_replicated_results(summary_file: Path) -> pd.DataFrame:
    """Carga y estandariza la tabla resumen de la replicacion."""
    if not summary_file.exists():
        raise FileNotFoundError(
            f"No se encontro el resumen esperado en: {summary_file}. "
            "Ejecuta primero scripts/02_generate_figure.py"
        )

    rep = pd.read_csv(summary_file)
    required_cols = {"subgroup", "control_mean_pct", "treat_mean_pct"}
    missing = sorted(required_cols - set(rep.columns))
    if missing:
        raise ValueError(f"Faltan columnas requeridas en el resumen: {missing}")

    return rep.rename(
        columns={
            "control_mean_pct": "control_rep",
            "treat_mean_pct": "treat_rep",
        }
    )


def build_validation_table(rep: pd.DataFrame) -> pd.DataFrame:
    """Combina referencia del paper con la replica y calcula discrepancias."""
    paper = build_paper_reference()

    comparison = paper.merge(
        rep[["subgroup", "control_rep", "treat_rep"]],
        on="subgroup",
        how="left",
        validate="one_to_one",
    )

    if comparison[["control_rep", "treat_rep"]].isna().any().any():
        missing_subgroups = comparison.loc[
            comparison["control_rep"].isna() | comparison["treat_rep"].isna(),
            "subgroup",
        ].tolist()
        raise ValueError(
            "No se encontraron resultados replicados para subgrupos: "
            f"{missing_subgroups}"
        )

    comparison["control_diff"] = comparison["control_rep"] - comparison["control_paper"]
    comparison["treat_diff"] = comparison["treat_rep"] - comparison["treat_paper"]
    comparison["abs_control_diff"] = comparison["control_diff"].abs()
    comparison["abs_treat_diff"] = comparison["treat_diff"].abs()

    return comparison


def save_plot(comparison: pd.DataFrame, output_plot: Path, dpi: int) -> None:
    """Guarda grafico de discrepancias entre paper y replica."""
    output_plot.parent.mkdir(parents=True, exist_ok=True)

    plot_df = comparison.set_index("panel_paper")[["control_diff", "treat_diff"]]
    ax = plot_df.plot(kind="bar", figsize=(10, 5))
    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylabel("Diferencia (puntos porcentuales)")
    ax.set_xlabel("Panel")
    ax.set_title("Diferencias entre resultados del paper y replica")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(output_plot, dpi=dpi, bbox_inches="tight")
    plt.close()


def build_journal_table(comparison: pd.DataFrame) -> pd.DataFrame:
    """Construye tabla resumen estilo journal con diferencias paper vs replica."""
    table = comparison[
        [
            "panel_paper",
            "control_paper",
            "control_rep",
            "treat_paper",
            "treat_rep",
        ]
    ].copy()
    table = table.rename(columns={"panel_paper": "panel"})

    table["diff_paper"] = table["control_paper"] - table["treat_paper"]
    table["diff_rep"] = table["control_rep"] - table["treat_rep"]
    return table


def save_journal_table_image(table: pd.DataFrame, output_file: Path, dpi: int) -> None:
    """Guarda la tabla de validacion como imagen en la carpeta de figuras."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    table_to_render = table.copy()
    numeric_cols = [col for col in table_to_render.columns if col != "panel"]
    table_to_render[numeric_cols] = table_to_render[numeric_cols].round(2)

    fig_height = max(2.8, 0.52 * len(table_to_render) + 1.1)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    ax.axis("off")

    mpl_table = ax.table(
        cellText=table_to_render.values,
        colLabels=table_to_render.columns,
        loc="center",
        cellLoc="center",
    )
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(9)
    mpl_table.scale(1, 1.25)

    for (row, _col), cell in mpl_table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#E8EDF5")

    plt.title("Tabla de validacion: paper vs replica", fontsize=11, pad=10)
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    config = Config()

    rep = load_replicated_results(config.input_summary)
    comparison = build_validation_table(rep)

    config.output_comparison.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(config.output_comparison, index=False)

    save_plot(comparison, config.output_plot, dpi=config.dpi)
    journal_table = build_journal_table(comparison)
    save_journal_table_image(journal_table, config.output_table_image, dpi=config.dpi)

    print("\n=== Validacion de resultados ===")
    print(
        comparison[
            [
                "panel_paper",
                "control_paper",
                "control_rep",
                "control_diff",
                "treat_paper",
                "treat_rep",
                "treat_diff",
            ]
        ].to_string(index=False)
    )

    print(
        "\nMaxima discrepancia absoluta (control): "
        f"{comparison['abs_control_diff'].max():.3f}"
    )
    print(
        "Maxima discrepancia absoluta (treatment): "
        f"{comparison['abs_treat_diff'].max():.3f}"
    )

    print("\n=== Tabla estilo journal ===")
    print(journal_table.round(2).to_string(index=False))

    print(f"\nTabla de validacion guardada en: {config.output_comparison}")
    print(f"Grafico de discrepancias guardado en: {config.output_plot}")
    print(f"Imagen de tabla guardada en: {config.output_table_image}")


if __name__ == "__main__":
    main()
