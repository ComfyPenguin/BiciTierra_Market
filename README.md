# BiciTierra Market · Proyecto de Machine Learning

Repositorio de trabajo para un caso práctico de **análisis de datos, predicción mensual de ventas y segmentación de clientes** con datos sintéticos de BiciTierra Market.

## Objetivo del proyecto

Desarrollar un flujo completo de análisis en tres bloques:

1. **EDA (Análisis Exploratorio de Datos)** para revisar calidad, cobertura temporal y patrones.
2. **Modelado baseline** para predecir `sales_units` del mes siguiente por combinación de canal, línea de producto y región.
3. **Segmentación de clientes** para obtener perfiles útiles para negocio.

## Estructura del repositorio

```text
BiciTierra_Market/
├── data/
│   ├── customers.csv
│   ├── sales_forecast_input.csv
│   └── sales_history.csv
└── notebooks/
    ├── 01_eda.ipynb
    ├── 02_modelatge_baseline.ipynb
    └── 03_segmentacio.ipynb
```

## Datasets

Todos los datos son **sintéticos** y orientados a docencia.

- `sales_history.csv`: histórico mensual (enero 2021 a junio 2026) para EDA y modelado.
- `sales_forecast_input.csv`: entradas de julio 2026 para aplicar el modelo entrenado.
- `customers.csv`: fotografía de clientes para tareas de segmentación.

## Notebooks

- `01_eda.ipynb`: exploración inicial, calidad de datos, cobertura y estacionalidad.
- `02_modelatge_baseline.ipynb`: creación de retardos temporales, comparación de referencias y modelo baseline.
- `03_segmentacio.ipynb`: segmentación de clientes con enfoque práctico de negocio.

## Enfoque metodológico recomendado

- Respetar la **separación temporal** (train/valid/test) para evitar fuga de información.
- Usar solo variables disponibles antes del mes a predecir.
- Evaluar con métricas de error interpretables para negocio (por ejemplo MAE y WAPE).
- Mantener trazabilidad de decisiones y resultados en los notebooks.

## Requisitos de entorno

- Python 3.10+
- Jupyter Notebook / JupyterLab
- Bibliotecas principales:
  - `pandas`
  - `numpy`
  - `matplotlib` (si se usan visualizaciones)
  - `scikit-learn` (si se amplía el modelado)

Instalación rápida:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter
```

## Cómo ejecutar

1. Abrir este repositorio en tu entorno local.
2. Iniciar Jupyter desde la raíz del proyecto.
3. Ejecutar los notebooks en este orden:
   1. `notebooks/01_eda.ipynb`
   2. `notebooks/02_modelatge_baseline.ipynb`
   3. `notebooks/03_segmentacio.ipynb`

## Referencia de documentación

La estructura pedagógica y criterios de trabajo se basan en los materiales de:

- https://github.com/ieseljust/iabd-26-27/
