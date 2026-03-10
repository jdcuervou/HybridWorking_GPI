## Processed data

Esta carpeta se reserva para datasets intermedios o transformados.

## Estado actual
En la version actual de la replica, el flujo principal consume `data/raw/figure2.csv`
y genera salidas directamente en `results/`, por lo que esta carpeta puede estar vacia.

## Uso futuro esperado
Guardar aqui archivos derivados como:
- Limpiezas estandarizadas.
- Variables construidas para analisis extendido.
- Tablas intermedias reutilizables.

## Recomendaciones de versionado
- Versionar solo procesados pequenos y estables que mejoren la reproducibilidad.
- Evitar versionar archivos grandes o temporales; regenerarlos con scripts.
