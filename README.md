# BiciTierra Market · Proyecto de Machine Learning

Repositorio de trabajo para un caso práctico de **análisis de datos, predicción mensual de ventas y segmentación de clientes** con datos sintéticos de BiciTierra Market.

## Objetivo

Predecir las unidades vendidas de cada serie comercial un mes antes de que empiece,
y segmentar a los clientes de BiciTierra Market. Los datos son sintéticos
(66 meses, 18 series comerciales): los resultados no son una previsión de mercado real.

El trabajo se organiza en tres bloques:

1. **EDA (Análisis Exploratorio de Datos)** para revisar calidad, cobertura temporal y patrones.
2. **Modelado baseline** para predecir `sales_units` del mes siguiente por combinación de canal, línea de producto y región.
3. **Segmentación de clientes** para obtener perfiles útiles para negocio.

## Miembros

| Nombre | Rol |
|--------|-----|
| Andy | _Pendiente_ |
| Guillem | _Pendiente_ |
| Dennis | _Pendiente_ |
## Estructura

```
BiciTierra_Market/
  README.md
  docs/                memoria, decisiones y seguimiento
  data/
    originales/        CSV originales, sin modificar
    derivados/         datos generados por los notebooks
  notebooks/           exploración, modelado y segmentación
  src/                 funciones reutilizables
  tests/               comprobaciones de datos o código
  evidencies/          métricas, predicciones, capturas y resultados del panel
```

Los datos originales no se sobrescriben nunca: cualquier transformación se guarda en `data/derivados/`.

## Datasets

Todos los datos son **sintéticos** y orientados a docencia. Están en `data/originales/`
y su diccionario de datos en `data/originales/DICCIONARI_DADES.md`.

- `sales_history.csv`: histórico mensual (enero 2021 a junio 2026) para EDA y modelado.
- `sales_forecast_input.csv`: entradas de julio 2026 para aplicar el modelo entrenado.
- `customers.csv`: fotografía de clientes para tareas de segmentación.

## Dependencias

El entorno de Python se gestiona con [uv](https://docs.astral.sh/uv/). Las dependencias
(`pandas`, `numpy`, `matplotlib`, `scikit-learn`, `jupyter`, `ipykernel`) están en
`pyproject.toml` y `uv.lock`; uv descarga la versión de Python necesaria si no la tienes.

### Iniciar el entorno

```bash
# 1. Instalar uv (si no lo tienes): https://docs.astral.sh/uv/getting-started/installation/
# 2. Crear .venv e instalar las dependencias
uv sync
# 3. Lanzar Jupyter
uv run jupyter lab
```

Para usarlo desde VS Code u otro editor, selecciona el intérprete `.venv/bin/python`
como kernel del notebook. Si quieres registrarlo como kernel de Jupyter:

```bash
uv run python -m ipykernel install --user --name bicitierra --display-name "BiciTierra (.venv)"
```

Para añadir una librería nueva: `uv add <paquete>` (y commitea `pyproject.toml` y `uv.lock`).

## Orden de ejecución

Ejecutar los notebooks desde la carpeta `notebooks/` (las rutas son relativas a ella:
`../data/originales/`).

1. `notebooks/01_eda.ipynb`: exploración inicial, calidad de datos, cobertura y estacionalidad.
2. `notebooks/02_modelatge_baseline.ipynb`: retardos temporales y modelos de referencia
   (media de grupo, mismo mes del año anterior y regresión lineal regularizada).
3. `notebooks/03_segmentacio.ipynb`: segmentación de clientes con enfoque práctico de negocio.

## Enfoque metodológico

- Respetar la **separación temporal** (train/valid/test) para evitar fuga de información.
- Usar solo variables disponibles antes del mes a predecir.
- Evaluar con métricas de error interpretables para negocio (por ejemplo MAE y WAPE).
- Mantener trazabilidad de decisiones y resultados en los notebooks.

## Limitaciones

- Datos sintéticos: una correlación encontrada aquí no demuestra una causa en el mundo real.
- El modelado excluye variables no conocidas antes del mes a predecir
  (sesiones, ingresos, gasto real, descuento real, stock final y rotura del mismo mes).
- En el paquete entregado los notebooks leían los CSV desde `../dades/`; en este
  repositorio se han adaptado a `../data/originales/`.

## Referencia de documentación

La estructura pedagógica y criterios de trabajo se basan en los materiales de:

- [Proyecto + Documentación de este año](https://comfypenguin.github.io/iabd-26-27/)
- [Documentación de años anteriores](https://fideldam2021.github.io/SAA2526/)
- [Documentación de años anteriores de programación IA](https://ce-bdia.github.io/pia/)
