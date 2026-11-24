"""Genera la presentación interactiva de la defensa en evidencies/presentacion.html.

Uso, desde la raíz del repositorio y después de ejecutar los notebooks:
    uv run python src/presentacion.py

Las notas del modo presentador (tecla N) salen de docs/defensa.md: si cambia el guion,
basta con volver a ejecutar este script.
"""
import json
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone

from modelo import ARCHIVO_MODELO, con_retrasos, historico, prever, variables

RAIZ = Path(__file__).resolve().parent.parent
ORIGINALES = RAIZ / 'data' / 'originales'
DERIVADOS = RAIZ / 'data' / 'derivados'
EVIDENCIAS = RAIZ / 'evidencies'
KEY = ['channel', 'product_line', 'region']

ventas = pd.read_csv(ORIGINALES / 'sales_history.csv')
metricas = pd.read_csv(EVIDENCIAS / 'metricas_modelos.csv')
prueba = pd.read_csv(EVIDENCIAS / 'prediccions_prova_2026.csv')
simulador = pd.read_csv(EVIDENCIAS / 'simulador_julio.csv')
julio = pd.read_csv(EVIDENCIAS / 'prediccions_juliol_2026.csv')
perfil = pd.read_csv(EVIDENCIAS / 'perfil_segmentos.csv')
clientes = pd.read_csv(ORIGINALES / 'customers.csv').merge(
    pd.read_csv(DERIVADOS / 'segmentos_clientes.csv'), on='customer_id', validate='one_to_one')
guion = (RAIZ / 'docs' / 'defensa.md').read_text(encoding='utf-8')

# Orden fijo de las 18 series: canal, línea y región (el mismo en todas las diapositivas)
orden = pd.MultiIndex.from_product([['store', 'ecommerce'], ['urban', 'mountain', 'electric'],
                                    ['coast', 'inland', 'metro']], names=KEY)

# Notas del presentador: «**N · Título (m:ss).** texto» y la tabla de reparto del guion
notas = {int(n): {'titulo': t, 'tiempo': tm, 'texto': tx.strip()}
         for n, t, tm, tx in re.findall(r'\*\*(\d+) · (.+?) \((\d+:\d+)\)\.\*\* (.+)', guion)}
for inicio, fin, quien in re.findall(r'\| (\d+)–(\d+) \| (\w+) \|', guion):
    for n in range(int(inicio), int(fin) + 1):
        notas[n]['quien'] = quien
plantilla = (RAIZ / 'src' / 'presentacion_plantilla.html').read_text(encoding='utf-8')
total = plantilla.count('<section class="diapo')
assert sorted(notas) == list(range(1, total + 1)), f'El guion debe tener las {total} diapositivas de la plantilla'

# Histórico: una fila por serie con sus 66 meses
def por_serie(columna):
    return ventas.pivot(index=KEY, columns='month', values=columna).reindex(orden)

unidades, roturas, stock = por_serie('sales_units'), por_serie('stockout'), por_serie('stock_units')
series = [{'canal': c, 'linea': l, 'region': r,
           'ventas': unidades.loc[(c, l, r)].astype(int).tolist(),
           'rotura': roturas.loc[(c, l, r)].astype(int).tolist(),
           'stock': stock.loc[(c, l, r)].astype(int).tolist()} for c, l, r in orden]

# Hipótesis, medidas solo con el periodo de entrenamiento (hasta 2024)
anio, mes = ventas['month'].str[:4].astype(int), ventas['month'].str[5:].astype(int)
entreno = ventas[anio <= 2024]
montana = entreno[entreno['product_line'] == 'mountain'].groupby('month')['sales_units'].sum()
montana_mes = montana.groupby(montana.index.str[5:]).mean()
electrica = entreno[entreno['product_line'] == 'electric'].groupby(anio)['sales_units'].sum()

# Fuga de información: reconstruir las unidades de 2025 con revenue (igual que en el notebook 02)
valid = ventas[anio == 2025]
estimacion = valid['revenue'] / (valid['list_price'] * (1 - valid['avg_discount']))
mae_fuga = float((valid['sales_units'] - estimacion).abs()[estimacion.notna()].mean())

# Modelos: el elegido es el que se probó en 2026; la referencia es la mejor de las dos simples
validacion = metricas[metricas['periodo'].str.startswith('validación')].set_index('model')
en_prueba = metricas[metricas['periodo'].str.startswith('prueba')].set_index('model')
elegido = en_prueba.index[0]
referencia = validacion.loc[['group_mean', 'seasonal_lag12'], 'MAE_units'].idxmin()

# Prueba ene–jun 2026: totales por mes y el peor caso
prueba['month'] = prueba['month'].str[:7]
prueba_mes = prueba.groupby('month')[['sales_units', 'prediccion']].sum()
peor = prueba.loc[(prueba['prediccion'] - prueba['sales_units']).abs().idxmax()]

# Simulador de julio: misma regla que el notebook (recortar entre 0 y el stock y redondear)
simulador = simulador.set_index(KEY).reindex(orden).reset_index()
recortada = np.rint(np.clip(simulador['prevision_sin_recortar'], 0, simulador['stock_units']))
assert recortada.sum() == julio['predicted_sales_units'].sum(), 'El simulador no reproduce la previsión'

# Clientes: el gasto que falta se reconstruye como en el notebook 03 (ticket × pedidos)
SEGMENTOS = {
    'fieles_veteranos': ('Fieles veteranos', 'Fidelizar: que sigan sintiéndose cuidados'),
    'nuevos_activos': ('Nuevos activos', 'Dar la bienvenida al segundo año'),
    'ocasionales_inactivos': ('Ocasionales inactivos', 'Reactivar con el servicio técnico'),
    'devoluciones_altas': ('Devoluciones altas', 'Revisar por qué devuelven'),
}
clientes['annual_spend'] = clientes['annual_spend'].fillna(
    (clientes['avg_order_value'] * clientes['orders_last_12m']).round(2))
visibles = clientes.dropna(subset=['days_since_last_order'])
indice = {clave: i for i, clave in enumerate(SEGMENTOS)}
perfil = perfil.set_index('cluster').reindex(list(SEGMENTOS))

# Puesta en marcha: se abre el modelo de scikit-learn que guarda src/modelo.py para enseñar qué hace cada paso
assert ARCHIVO_MODELO.exists(), 'Falta el modelo: ejecuta antes «uv run python src/modelo.py entrenar»'
modelo = joblib.load(ARCHIVO_MODELO)
preparar, escalar, ridge = (paso for _, paso in modelo.steps)
filas = con_retrasos(historico(), historico()).dropna(subset=['lag_1', 'lag_12'])
entreno_sk = filas[filas['month'] < '2025-01-01']
valid_sk = filas[filas['month'].dt.year == 2025]
columnas = [n.split('__', 1)[1] for n in preparar.get_feature_names_out()]

ES = {'marketing_budget': 'presupuesto', 'planned_discount': 'descuento previsto', 'stock_units': 'stock inicial',
      'list_price': 'precio de tarifa', 'days_in_month': 'días del mes', 'lag_1': 'ventas del mes anterior',
      'lag_12': 'ventas de hace un año', 'month_sin': 'temporada (seno)', 'month_cos': 'temporada (coseno)',
      'time_index': 'tendencia', 'store': 'tienda', 'ecommerce': 'online', 'urban': 'urbana', 'mountain': 'montaña',
      'electric': 'eléctrica', 'coast': 'costa', 'inland': 'interior', 'metro': 'metro', 'none': 'ninguna',
      'spring': 'primavera', 'summer': 'verano', 'black_friday': 'Black Friday', 'christmas': 'Navidad',
      'channel': 'canal', 'product_line': 'línea', 'region': 'región', 'campaign': 'campaña'}

def legible(columna):
    """'region_inland' → 'región: interior'; 'urban_cos' → 'temporada urbana (coseno)'."""
    if columna in ES:
        return ES[columna]
    for campo in KEY + ['campaign']:
        if columna.startswith(campo + '_'):
            return f"{ES[campo]}: {ES[columna[len(campo) + 1:]]}"
    linea, onda = columna.split('_')
    return f"temporada {ES[linea]} ({'seno' if onda == 'sin' else 'coseno'})"

# La fila de ejemplo que recorre el Pipeline: julio 2022, online, urbana, costa (le falta el presupuesto)
ejemplo = entreno_sk[(entreno_sk['month'] == '2022-07-01') & (entreno_sk['channel'] == 'ecommerce')
                     & (entreno_sk['product_line'] == 'urban') & (entreno_sk['region'] == 'coast')]
assert len(ejemplo) == 1 and ejemplo['marketing_budget'].isna().all()
abierta = preparar.transform(variables(ejemplo))[0]   # tras SimpleImputer + OneHotEncoder
z = escalar.transform(abierta.reshape(1, -1))[0]      # tras StandardScaler
aportes = pd.Series(ridge.coef_ * z, index=columnas)
principales = aportes.reindex(aportes.abs().sort_values(ascending=False).index[:5])
fila = ejemplo.iloc[0]
assert abs(ridge.intercept_ + aportes.sum() - modelo.predict(variables(ejemplo))[0]) < 1e-6

# Efecto de alpha: el mismo Pipeline reentrenado con otros valores (solo para la explicación)
coef = pd.Series(ridge.coef_, index=columnas)
top = coef.abs().sort_values(ascending=False).index[:8]
alphas = [1, 10, 100, 1000, 10000]
recorrido = []
for alpha in alphas:
    otro = clone(modelo).set_params(ridge__alpha=alpha).fit(variables(entreno_sk), entreno_sk['sales_units'])
    error = np.abs(valid_sk['sales_units'].to_numpy() - prever(otro, valid_sk)).mean()
    recorrido.append({'alpha': alpha, 'mae': float(error),
                      'coef': pd.Series(otro.steps[-1][1].coef_, index=columnas)[top].round(2).tolist()})

nulos_entreno = entreno_sk[['marketing_budget', 'planned_discount']].isna()
rejilla = entreno_sk.assign(nulo=nulos_entreno.any(axis=1).astype(int))
entrenamiento = {
    'filas': len(entreno_sk), 'columnas': len(columnas), 'nulos': int(nulos_entreno.sum().sum()),
    'archivo_kb': round(ARCHIVO_MODELO.stat().st_size / 1024, 1),
    'mediana_presupuesto': float(preparar.named_transformers_['numericas'].statistics_[0]),
    'ventas': rejilla.pivot(index=KEY, columns='month', values='sales_units').reindex(orden).astype(int).values.tolist(),
    'nulo': rejilla.pivot(index=KEY, columns='month', values='nulo').reindex(orden).astype(int).values.tolist(),
    'ejemplo': {'mes': '2022-07', 'canal': fila['channel'], 'linea': fila['product_line'], 'region': fila['region'],
                'campana': ES[fila['campaign']], 'descuento': float(fila['planned_discount']),
                'stock': int(fila['stock_units']), 'lag_1': int(fila['lag_1']), 'lag_12': int(fila['lag_12']),
                'ventas': int(fila['sales_units']),
                # Columnas que solo se conocen al cierre del mes: se enseñan para ver que se quedan fuera de X
                'revenue': float(fila['revenue']), 'stock_final': int(fila['closing_stock_units']),
                'sesiones': None if pd.isna(fila['website_sessions']) else int(fila['website_sessions'])},
    'onehot': [{'campo': ES[campo], 'valor': ES[c[len(campo) + 1:]], 'uno': int(abierta[i])}
               for i, c in enumerate(columnas) for campo in KEY + ['campaign'] if c.startswith(campo + '_')],
    'escala': [{'nombre': ES[c], 'crudo': float(abierta[columnas.index(c)]), 'z': float(z[columnas.index(c)])}
               for c in ['marketing_budget', 'planned_discount', 'stock_units', 'lag_12']],
    'top': [legible(c) for c in top],
    'recorrido': recorrido,
    'aportes': {'base': float(ridge.intercept_),
                'principales': [{'nombre': legible(c), 'valor': float(v)} for c, v in principales.items()],
                'resto': float(aportes.drop(principales.index).sum()),
                'prevision': int(np.rint(prever(modelo, ejemplo)[0])), 'real': int(fila['sales_units'])},
}

julio_linea = julio.groupby('product_line')['predicted_sales_units'].sum()
datos = {
    'notas': notas,
    'meses': sorted(ventas['month'].unique()),
    'series': series,
    'por_linea': {l: unidades.xs(l, level='product_line').sum().astype(int).tolist() for l in ['urban', 'mountain', 'electric']},
    'julio_por_linea': {l: int(v) for l, v in julio_linea.items()},
    'kpi': {
        'meses': int(ventas['month'].nunique()),
        'series': len(orden),
        'clientes': len(clientes),
        'rotura_pct': round(100 * ventas['stockout'].mean()),
        'nulos': int(ventas.isna().sum().sum()),
        'columnas_con_nulos': int((ventas.isna().sum() > 0).sum()),
        'ratio_montana': round(float(montana_mes['07'] / montana_mes['01']), 1),
        'crecimiento_electrica': round(float(100 * (electrica[2024] / electrica[2021] - 1))),
        'mae_fuga': mae_fuga,
        'prevision_julio': int(julio['predicted_sales_units'].sum()),
        'stock_julio': int(simulador['stock_units'].sum()),
        'mae_valid': float(validacion.loc[elegido, 'MAE_units']),
        'mae_ref': float(validacion.loc[referencia, 'MAE_units']),
        'mejora_pct': round(float(100 * (1 - validacion.loc[elegido, 'MAE_units'] / validacion.loc[referencia, 'MAE_units']))),
        'mae_prueba': float(en_prueba.loc[elegido, 'MAE_units']),
        'wape_prueba': float(en_prueba.loc[elegido, 'WAPE_pct']),
        'mae_ref_prueba': float(en_prueba.loc[referencia, 'MAE_units']),
        'sesgo': abs(round(float((prueba['prediccion'] - prueba['sales_units']).mean()))),
        'clientes_visibles': len(visibles),
        'segmentos': len(SEGMENTOS),
    },
    'elegido': elegido,
    'entrenamiento': entrenamiento,
    'modelos': metricas.to_dict('records'),
    'prueba': {
        'meses': prueba_mes.index.tolist(),
        'real': prueba_mes['sales_units'].astype(int).tolist(),
        'prevista': prueba_mes['prediccion'].round().astype(int).tolist(),
        'sesgo': round(float((prueba['prediccion'] - prueba['sales_units']).mean()), 1),
        'peor': {'mes': peor['month'], 'canal': peor['channel'], 'linea': peor['product_line'],
                 'region': peor['region'], 'real': int(peor['sales_units']), 'prevista': int(round(peor['prediccion']))},
    },
    'simulador': [{'canal': f['channel'], 'linea': f['product_line'], 'region': f['region'],
                   'stock': int(f['stock_units']), 'presupuesto': f['marketing_budget'], 'descuento': f['planned_discount'],
                   'base': f['prevision_sin_recortar'], 'ef_presupuesto': f['efecto_marketing_budget'],
                   'ef_descuento': f['efecto_planned_discount'], 'ef_stock': f['efecto_stock_units']}
                  for f in simulador.to_dict('records')],
    'segmentos': [{'clave': clave, 'nombre': nombre, 'accion': accion,
                   'clientes': int(perfil.loc[clave, 'clientes']),
                   'gasto': float(perfil.loc[clave, 'gasto_mediano']),
                   'pedidos': float(perfil.loc[clave, 'pedidos_medianos']),
                   'recencia': float(perfil.loc[clave, 'recencia_mediana']),
                   'devoluciones': float(perfil.loc[clave, 'devoluciones_medias']),
                   'antiguedad': float(perfil.loc[clave, 'antiguedad_mediana'])}
                  for clave, (nombre, accion) in SEGMENTOS.items()],
    # Cada cliente como lista corta: [gasto, días sin comprar, segmento, id, pedidos, % devoluciones]
    'clientes': [[round(f.annual_spend), int(f.days_since_last_order), indice[f.segmento], f.customer_id,
                  int(f.orders_last_12m), round(100 * f.returns_ratio)] for f in visibles.itertuples()],
}

salida = EVIDENCIAS / 'presentacion.html'
salida.write_text(plantilla.replace('__DATOS__', json.dumps(datos, ensure_ascii=False)), encoding='utf-8')
print('Presentación guardada en', salida)
