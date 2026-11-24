"""Genera el panel de BiciTierra Market en evidencies/panel.html.

Uso, desde la raíz del repositorio y después de ejecutar los notebooks:
    uv run python src/panel.py
"""
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ORIGINALES = RAIZ / 'data' / 'originales'
EVIDENCIAS = RAIZ / 'evidencies'

ventas = pd.read_csv(ORIGINALES / 'sales_history.csv')
metricas = pd.read_csv(EVIDENCIAS / 'metricas_modelos.csv')
julio = pd.read_csv(EVIDENCIAS / 'prediccions_juliol_2026.csv')
entrada_julio = pd.read_csv(ORIGINALES / 'sales_forecast_input.csv')
perfil = pd.read_csv(EVIDENCIAS / 'perfil_segmentos.csv', index_col=0)

# Ventas observadas: solo se suman unidades, nunca precios ni porcentajes
mensual = ventas.pivot_table(index='month', columns='product_line', values='sales_units', aggfunc='sum')
julio['month'] = julio['month'].str[:7]
prevision = julio.groupby('product_line')['predicted_sales_units'].sum()

ventas_2025 = ventas[ventas['month'].str.startswith('2025')]
canal_producto = ventas_2025.pivot_table(index='product_line', columns='channel', values='sales_units', aggfunc='sum')

julio = julio.merge(entrada_julio[['channel', 'product_line', 'region', 'stock_units']],
                    on=['channel', 'product_line', 'region'], validate='one_to_one')
julio['en_limite'] = julio['predicted_sales_units'] >= julio['stock_units']

prueba = metricas[metricas['periodo'].str.startswith('prueba')].set_index('model')
elegido = prueba.index[0]

datos = {
    'meses': list(mensual.index) + ['2026-07'],
    'lineas': {linea: [int(v) for v in mensual[linea]] + [None] for linea in mensual.columns},
    'prevision': {linea: [None] * (len(mensual) - 1) + [int(mensual[linea].iloc[-1]), int(prevision[linea])]
                  for linea in mensual.columns},
    'canal_producto': {'productos': list(canal_producto.index),
                       'canales': {c: [int(v) for v in canal_producto[c]] for c in canal_producto.columns}},
    'modelos': metricas.round(2).to_dict('records'),
    'segmentos': perfil.reset_index().round(2).to_dict('records'),
    'julio': julio.to_dict('records'),
    'kpi': {
        'ventas_2025': int(ventas_2025['sales_units'].sum()),
        'mae_prueba': float(prueba.loc[elegido, 'MAE_units'].round(1)),
        'wape_prueba': float(prueba.loc[elegido, 'WAPE_pct'].round(1)),
        'prevision_julio': int(julio['predicted_sales_units'].sum()),
        'clientes': int(perfil['clientes'].sum()),
        'modelo': elegido,
    },
}

plantilla = (RAIZ / 'src' / 'panel_plantilla.html').read_text(encoding='utf-8')
(EVIDENCIAS / 'panel.html').write_text(plantilla.replace('__DATOS__', json.dumps(datos, ensure_ascii=False)), encoding='utf-8')
print('Panel guardado en', EVIDENCIAS / 'panel.html')
