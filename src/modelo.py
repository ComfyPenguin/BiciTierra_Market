"""Pone en marcha el modelo de ventas con scikit-learn.

Uso, desde la raíz del repositorio:
    uv run python src/modelo.py entrenar   # aprende con 2022–2024, lo mide en 2025 y 2026 y lo guarda
    uv run python src/modelo.py predecir   # carga el modelo guardado y predice julio de 2026

Es el mismo modelo que el notebook 02 (ridge con alpha = 100 y las mismas variables),
pero montado como Pipeline de scikit-learn y guardado en evidencies/modelo_ridge.joblib.
"""
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / 'data' / 'originales'
ARCHIVO_MODELO = RAIZ / 'evidencies' / 'modelo_ridge.joblib'

KEY = ['channel', 'product_line', 'region']
LINEAS = ['urban', 'mountain', 'electric']
# Solo variables que se conocen antes de que empiece el mes
NUMERICAS = (['marketing_budget', 'planned_discount', 'stock_units', 'list_price', 'days_in_month',
              'lag_1', 'lag_12', 'month_sin', 'month_cos', 'time_index']
             + [f'{linea}_{onda}' for linea in LINEAS for onda in ('sin', 'cos')])
CATEGORIAS = KEY + ['campaign']


def historico():
    ventas = pd.read_csv(DATOS / 'sales_history.csv')
    ventas['month'] = pd.to_datetime(ventas['month'], format='%Y-%m')
    return ventas


def con_retrasos(filas, ventas):
    """Añade lag_1 y lag_12: lo vendido por la misma serie 1 y 12 meses antes."""
    for lag in [1, 12]:
        pasado = ventas[['month'] + KEY + ['sales_units']].copy()
        pasado['month'] = pasado['month'] + pd.DateOffset(months=lag)
        filas = filas.merge(pasado.rename(columns={'sales_units': f'lag_{lag}'}),
                            on=['month'] + KEY, how='left', validate='one_to_one')
    return filas


def variables(filas):
    """Estacionalidad (mes como círculo, también por línea) y tendencia, igual que design() del notebook."""
    x = filas.copy()
    mes = x['month'].dt.month
    x['month_sin'] = np.sin(2 * np.pi * mes / 12)
    x['month_cos'] = np.cos(2 * np.pi * mes / 12)
    x['time_index'] = (x['month'].dt.year - 2021) * 12 + mes - 1
    for linea in LINEAS:
        x[f'{linea}_sin'] = x['month_sin'] * (x['product_line'] == linea)
        x[f'{linea}_cos'] = x['month_cos'] * (x['product_line'] == linea)
    return x[NUMERICAS + CATEGORIAS]


def nuevo_modelo():
    """Nulos con la mediana, categorías en columnas 0/1, todo escalado y ridge con alpha = 100."""
    preparar = ColumnTransformer([
        ('numericas', SimpleImputer(strategy='median'), NUMERICAS),
        ('categorias', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORIAS),
    ])
    return make_pipeline(preparar, StandardScaler(), Ridge(alpha=100))


def prever(modelo, filas):
    """Predice y recorta entre 0 y el stock: no se puede vender más de lo que hay."""
    return np.clip(modelo.predict(variables(filas)), 0, filas['stock_units'].to_numpy())


def entrenar():
    ventas = historico()
    datos = con_retrasos(ventas, ventas).dropna(subset=['lag_1', 'lag_12'])  # 2021 no tiene lag_12
    train = datos[datos['month'] < '2025-01-01']
    valid = datos[datos['month'].dt.year == 2025]
    test = datos[datos['month'] >= '2026-01-01']

    modelo = nuevo_modelo().fit(variables(train), train['sales_units'])
    print(modelo, '\n')
    print(f'Entrenado con {len(train)} filas (2022–2024)')

    notebook = pd.read_csv(RAIZ / 'evidencies' / 'metricas_modelos.csv').query("model == 'ridge_100'")
    for (nombre, parte), esperado in zip([('Validación 2025', valid), ('Prueba ene–jun 2026', test)],
                                         notebook['MAE_units']):
        error = np.abs(parte['sales_units'].to_numpy() - prever(modelo, parte))
        mae, wape = error.mean(), 100 * error.sum() / parte['sales_units'].sum()
        print(f'{nombre}: MAE {mae:.2f} bicis · WAPE {wape:.2f} % (notebook 02: MAE {esperado:.2f})')
        assert abs(mae - esperado) < 0.1, 'scikit-learn no reproduce el modelo del notebook'

    joblib.dump(modelo, ARCHIVO_MODELO)
    print('\nModelo guardado en', ARCHIVO_MODELO.relative_to(RAIZ))


def predecir():
    if not ARCHIVO_MODELO.exists():
        sys.exit('No hay modelo guardado: ejecuta antes «uv run python src/modelo.py entrenar»')
    modelo = joblib.load(ARCHIVO_MODELO)
    print('Modelo cargado de', ARCHIVO_MODELO.relative_to(RAIZ), '\n')

    julio = pd.read_csv(DATOS / 'sales_forecast_input.csv')
    julio['month'] = pd.to_datetime(julio['month'], format='%Y-%m')
    julio = con_retrasos(julio, historico())
    assert julio[['lag_1', 'lag_12']].notna().all().all(), 'Falta el histórico de alguna serie'

    julio['prevision'] = np.rint(prever(modelo, julio)).astype(int)
    julio['aviso'] = np.where(julio['prevision'] >= julio['stock_units'], 'llega al stock', '')
    print(julio[KEY + ['stock_units', 'prevision', 'aviso']].to_string(index=False))
    print(f"\nJulio 2026: {julio['prevision'].sum()} bicis previstas de {julio['stock_units'].sum()} en stock. "
          'Es una previsión, no un resultado.')


if __name__ == '__main__':
    ordenes = {'entrenar': entrenar, 'predecir': predecir}
    if len(sys.argv) != 2 or sys.argv[1] not in ordenes:
        sys.exit('Uso: uv run python src/modelo.py entrenar | predecir')
    ordenes[sys.argv[1]]()
