"""Prepara los datos de las gráficas de la presentación para Power BI en evidencies/powerbi_datos.xlsx.

Uso, desde la raíz del repositorio y después de ejecutar los notebooks:
    uv run python src/powerbi.py

Cada hoja es una tabla de Excel con los datos de una o varias gráficas de la presentación.
Se aplican las mismas reglas que en src/presentacion.py para que las cifras coincidan.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl.worksheet.table import Table, TableStyleInfo

RAIZ = Path(__file__).resolve().parent.parent
ORIGINALES = RAIZ / 'data' / 'originales'
DERIVADOS = RAIZ / 'data' / 'derivados'
EVIDENCIAS = RAIZ / 'evidencies'
KEY = ['channel', 'product_line', 'region']

# Los mismos nombres que usa la presentación
NOMBRE = {'store': 'Tienda', 'ecommerce': 'Online', 'urban': 'Urbana', 'mountain': 'Montaña',
          'electric': 'Eléctrica', 'coast': 'Costa', 'inland': 'Interior', 'metro': 'Metro'}
SEGMENTOS = {
    'fieles_veteranos': ('Fieles veteranos', 'Fidelizar: que sigan sintiéndose cuidados'),
    'nuevos_activos': ('Nuevos activos', 'Dar la bienvenida al segundo año'),
    'ocasionales_inactivos': ('Ocasionales inactivos', 'Reactivar con el servicio técnico'),
    'devoluciones_altas': ('Devoluciones altas', 'Revisar por qué devuelven'),
}
# Orden fijo de las 18 series (canal, línea, región), como en la presentación
ORDEN = [(c, l, r) for c in ['store', 'ecommerce'] for l in ['urban', 'mountain', 'electric']
         for r in ['coast', 'inland', 'metro']]


def en_castellano(df):
    """Traduce canal, línea y región y añade el nombre de la serie y su posición (1–18)."""
    posicion = {serie: i + 1 for i, serie in enumerate(ORDEN)}
    df['orden_serie'] = [posicion[t] for t in zip(df['channel'], df['product_line'], df['region'])]
    for col in KEY:
        df[col] = df[col].map(NOMBRE)
    df['serie'] = df['channel'] + ' · ' + df['product_line'] + ' · ' + df['region']
    return df.rename(columns={'channel': 'canal', 'product_line': 'linea', 'region': 'region'})


# Diapositivas 2, 3 y 4: histórico de ventas y roturas por serie y mes
ventas = pd.read_csv(ORIGINALES / 'sales_history.csv')
ventas = en_castellano(ventas[['month'] + KEY + ['sales_units', 'stockout', 'stock_units']].copy())
ventas['mes'] = pd.to_datetime(ventas.pop('month'))
ventas = ventas.rename(columns={'sales_units': 'unidades', 'stockout': 'rotura', 'stock_units': 'stock'})

# Diapositiva 6: error de cada modelo
modelos = pd.read_csv(EVIDENCIAS / 'metricas_modelos.csv').rename(
    columns={'model': 'modelo', 'MAE_units': 'mae', 'WAPE_pct': 'wape'})

# Diapositiva 7: prueba enero–junio 2026, real frente a previsto por serie
prueba = pd.read_csv(EVIDENCIAS / 'prediccions_prova_2026.csv')
prueba = en_castellano(prueba)
prueba['mes'] = pd.to_datetime(prueba.pop('month'))
prueba = prueba.rename(columns={'sales_units': 'real', 'prediccion': 'prevista'})

# Diapositiva 9: previsión de julio frente al stock de cada serie
julio = pd.read_csv(EVIDENCIAS / 'simulador_julio.csv')[KEY + ['stock_units']].merge(
    pd.read_csv(EVIDENCIAS / 'prediccions_juliol_2026.csv')[KEY + ['predicted_sales_units']],
    on=KEY, validate='one_to_one')
julio = en_castellano(julio).rename(columns={'stock_units': 'stock', 'predicted_sales_units': 'prevision'})
julio['llega_al_stock'] = np.where(julio['prevision'] >= julio['stock'], 'Sí', 'No')

# Diapositiva 10: perfil medio de cada segmento
perfil = pd.read_csv(EVIDENCIAS / 'perfil_segmentos.csv').set_index('cluster').reindex(list(SEGMENTOS))
perfil.insert(0, 'segmento', [n for n, _ in SEGMENTOS.values()])
perfil.insert(1, 'accion', [a for _, a in SEGMENTOS.values()])
perfil.insert(0, 'orden_segmento', range(1, len(SEGMENTOS) + 1))

# Diapositiva 11: un punto por cliente; el gasto que falta se reconstruye como en el notebook 03
clientes = pd.read_csv(ORIGINALES / 'customers.csv').merge(
    pd.read_csv(DERIVADOS / 'segmentos_clientes.csv'), on='customer_id', validate='one_to_one')
clientes['annual_spend'] = clientes['annual_spend'].fillna(
    (clientes['avg_order_value'] * clientes['orders_last_12m']).round(2))
clientes = clientes.dropna(subset=['days_since_last_order'])
clientes = pd.DataFrame({
    'cliente': clientes['customer_id'],
    'segmento': clientes['segmento'].map(lambda s: SEGMENTOS[s][0]),
    'gasto_anual': clientes['annual_spend'].round(),
    'dias_sin_comprar': clientes['days_since_last_order'].astype(int),
    'pedidos': clientes['orders_last_12m'],
    'devoluciones_pct': (100 * clientes['returns_ratio']).round(),
})

tablas = {'ventas': ventas, 'modelos': modelos, 'prueba': prueba, 'julio': julio,
          'segmentos': perfil.reset_index(drop=True), 'clientes': clientes}

salida = EVIDENCIAS / 'powerbi_datos.xlsx'
with pd.ExcelWriter(salida, engine='openpyxl') as libro:
    for nombre, df in tablas.items():
        df.to_excel(libro, sheet_name=nombre, index=False)
        # Power BI solo importa datos que estén en formato de tabla de Excel
        hoja = libro.sheets[nombre]
        tabla = Table(displayName=nombre, ref=hoja.dimensions)
        tabla.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
        hoja.add_table(tabla)
print('Datos para Power BI guardados en', salida)
