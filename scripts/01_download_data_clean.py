from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple
from urllib.parse import quote, urlparse
import io

import requests
import pandas as pd

# Importar configuración del proyecto
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import ProjectConfig, DATA_RAW_DIR


def safe_doi(doi: str) -> str:
    doi = doi.strip()
    if doi.lower().startswith("doi:"):
        doi = doi[4:]
    return doi


def resolve_doi(doi: str) -> str:
    response = requests.get(
        f"https://doi.org/{quote(doi, safe='/')}",
        headers={"Accept": "text/html"},
        allow_redirects=True,
        timeout=30,
    )
    response.raise_for_status()
    return response.url


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_stream(url: str, target_path: Path) -> None:
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        ensure_dir(target_path.parent)
        with target_path.open("wb") as file_handle:
            for chunk in response.iter_content(chunk_size=1024 * 256):
                if chunk:
                    file_handle.write(chunk)


def download_and_convert_to_csv(url: str, target_path: Path) -> None:
    """Descarga un archivo .tab y lo convierte a CSV."""
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    
    # Leer como archivo separado por tabs
    df = pd.read_csv(io.BytesIO(response.content), sep='\t')
    
    # Guardar como CSV
    ensure_dir(target_path.parent)
    df.to_csv(target_path, index=False)
    print(f"  Convertido a CSV: {df.shape[0]} filas, {df.shape[1]} columnas")


def dataverse_download_plan(base_url: str, doi: str, filter_pattern: str = None) -> Iterable[Tuple[str, Path]]:
    metadata_url = f"{base_url.rstrip('/')}/api/datasets/:persistentId"
    response = requests.get(metadata_url, params={"persistentId": f"doi:{doi}"}, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "OK":
        raise RuntimeError("No fue posible consultar metadatos en Dataverse.")

    data = payload.get("data", {})
    latest = data.get("latestVersion", {})
    files = latest.get("files", [])

    for item in files:
        data_file = item.get("dataFile", {})
        file_id = data_file.get("id")
        file_name = data_file.get("filename")
        if not file_id or not file_name:
            continue

        # Aplicar filtro si se especifica
        if filter_pattern and filter_pattern.lower() not in file_name.lower():
            continue

        # Guardar directamente en raw/ sin subcarpetas
        relative = Path(file_name)
        file_url = f"{base_url.rstrip('/')}/api/access/datafile/{file_id}"
        yield file_url, relative


def zenodo_download_plan(landing_url: str) -> Iterable[Tuple[str, Path]]:
    parsed = urlparse(landing_url)
    parts = [part for part in parsed.path.split("/") if part]
    if "records" not in parts:
        raise RuntimeError("No se pudo inferir el ID del registro de Zenodo desde la URL.")

    record_index = parts.index("records")
    if record_index + 1 >= len(parts):
        raise RuntimeError("No se encontró ID de registro en la URL de Zenodo.")

    record_id = parts[record_index + 1]
    api_url = f"{parsed.scheme}://{parsed.netloc}/api/records/{record_id}"
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    files = payload.get("files", [])
    for item in files:
        key = item.get("key")
        links = item.get("links", {})
        file_url = links.get("self")
        if not key or not file_url:
            continue
        yield file_url, Path(key)


def detect_source(landing_url: str) -> str:
    host = urlparse(landing_url).netloc.lower()
    if "zenodo.org" in host:
        return "zenodo"
    return "dataverse"


def execute_downloads(plan: Iterable[Tuple[str, Path]], output_dir: Path, convert_to_csv: bool = False) -> int:
    count = 0
    for file_url, relative_path in plan:
        # Cambiar extensión a .csv si es necesario
        if convert_to_csv and relative_path.suffix in ['.tab', '.tsv']:
            target = output_dir / relative_path.with_suffix('.csv')
        else:
            target = output_dir / relative_path
        
        print(f"Descargando: {relative_path.name} -> {target.name}")
        
        if convert_to_csv and relative_path.suffix in ['.tab', '.tsv']:
            download_and_convert_to_csv(file_url, target)
        else:
            download_stream(file_url, target)
        
        count += 1
    return count


def main() -> None:
    try:
        config = ProjectConfig()
        
        parser = argparse.ArgumentParser(
            description="Descarga archivos de un dataset a partir de un DOI (Dataverse o Zenodo)."
        )
        parser.add_argument(
            "--doi",
            default=config.doi,
            help=f"DOI del dataset. Por defecto: {config.doi}",
        )
        parser.add_argument(
            "--output-dir",
            default=str(DATA_RAW_DIR),
            help="Directorio donde se guardan los datos descargados.",
        )
        parser.add_argument(
            "--filter",
            default="figure2",
            help="Filtrar archivos por nombre (por defecto: figure2)",
        )
        parser.add_argument(
            "--convert-csv",
            action="store_true",
            default=True,
            help="Convertir archivos .tab a CSV (por defecto: True)",
        )
        args = parser.parse_args()

        doi = safe_doi(args.doi)
        output_dir = Path(args.output_dir).resolve()
        ensure_dir(output_dir)

        print(f"Resolviendo DOI: {doi}")
        print(f"Filtro de archivos: {args.filter}")
        
        try:
            landing_url = resolve_doi(doi)
        except Exception as e:
            raise RuntimeError(
                f"No se pudo resolver el DOI. Verifica tu conexión a internet.\n"
                f"Error: {str(e)}"
            )
        
        source = detect_source(landing_url)
        print(f"Fuente detectada: {source}")
        print(f"URL de aterrizaje: {landing_url}\n")

        if source == "zenodo":
            plan = zenodo_download_plan(landing_url)
        else:
            base_url = f"{urlparse(landing_url).scheme}://{urlparse(landing_url).netloc}"
            plan = dataverse_download_plan(base_url=base_url, doi=doi, filter_pattern=args.filter)

        total = execute_downloads(plan, output_dir, convert_to_csv=args.convert_csv)
        if total == 0:
            raise RuntimeError(
                f"No se encontraron archivos para descargar con el filtro '{args.filter}'.\n"
                f"Intenta sin filtro: --filter \"\""
            )

        print(f"\n✅ Descarga completada. Archivos descargados: {total}")
        print(f"Directorio destino: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ ERROR en descarga: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"\nVer TROUBLESHOOTING.md para más ayuda")
        raise


if __name__ == "__main__":
    main()
