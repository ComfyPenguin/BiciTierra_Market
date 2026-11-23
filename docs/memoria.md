# Memoria · BiciTierra Market

Equipo: Andy, Guillem y Dennis. Datos sintéticos: los resultados no son una previsión de mercado real.

## 1. Problema y preguntas

BiciTierra Market vende bicis urbanas, de montaña y eléctricas en tienda física y en línea, en tres regiones. La dirección quiere decidir mejor el stock y las campañas.

- **Pregunta principal:** ¿cuántas unidades venderemos el mes siguiente en cada combinación de canal, línea de producto y región, usando solo información disponible antes de que empiece el mes? **Decisión:** cuánto stock asignar a cada canal y región.
- **Pregunta secundaria:** ¿qué grupos de clientes se distinguen por gasto, frecuencia, recencia y devoluciones, y qué acción conviene a cada uno? **Decisión:** a quién dirigir campañas de fidelización, reactivación o servicio.

## 2. Datos y calidad

| Fichero | Contenido | Unidad de observación |
|---|---|---|
| `sales_history.csv` | 1 188 filas, enero 2021 – junio 2026 | Un mes × canal × línea × región (18 series de 66 meses) |
| `sales_forecast_input.csv` | 18 filas de julio 2026, sin objetivo | Igual que el histórico |
| `customers.csv` | 2 000 clientes, foto del 30/06/2026 | Un cliente |

Problemas detectados y decisiones:

| Problema | Decisión |
|---|---|
| Nulos en `marketing_spend`, `avg_discount`, `website_sessions` | No se usan: se conocen al cierre del mes |
| Nulos en `marketing_budget` y `planned_discount` | Mediana de entrenamiento, nunca 0 |
| Censura por stock (19 % de los meses con `stockout = 1`) | Se conservan; las predicciones se limitan entre 0 y el stock |
| 30 clientes sin `annual_spend` | Se reconstruye como `avg_order_value × orders_last_12m` |
| 20 clientes sin `days_since_last_order` | Mediana |

Los CSV originales no se modifican.

## 3. Hipótesis del análisis exploratorio

1. **Estacionalidad:** el pico de ventas va de primavera a julio. En julio, `mountain` vende 131 unidades de media frente a 63 en enero (2021–2024). No podemos separar el efecto de la campaña del de la estación.
2. **Tendencia:** `electric` (+28 % entre 2021 y 2024) y `ecommerce` crecen; `urban` y `store` se mantienen.

Las dos se confirman después: `lag_12` mejora a la media plana (hipótesis 1) y los mayores errores son crecimiento que el modelo no capta (hipótesis 2).

## 4. Predicción de ventas

**Partición temporal:** entrenamiento 2022–2024 (648 filas), validación 2025 (216), prueba enero–junio 2026 (108). 2021 solo se usa para calcular `lag_12`.

**Predictores admitidos** (conocidos antes del mes): canal, producto, región, campaña, stock inicial, presupuesto y descuento previstos, precio, días del mes, mes del año, `lag_1`, `lag_12` y tendencia. **Excluidos:** `revenue`, `website_sessions`, `marketing_spend`, `avg_discount`, `closing_stock_units` y `stockout`. Con `revenue` se reconstruyen las unidades con error 0: es una fuga de información.

**Comparativa en validación (2025):**

| Modelo | MAE (unidades) | WAPE |
|---|---|---|
| Media de la serie | 18,75 | 18,06 % |
| Mismo mes del año anterior | 17,40 | 16,77 % |
| Ridge, `alpha = 1` | 12,43 | 11,98 % |
| Ridge, `alpha = 10` | 12,37 | 11,92 % |
| **Ridge, `alpha = 100`** | **12,05** | **11,61 %** |

**Modelo elegido:** ridge con `alpha = 100`, solo con datos de validación. Reduce el error un 31 % frente a la mejor referencia.

**Comprobación de la elección:** con validación cruzada temporal (entrenar con el pasado y validar 2023, 2024 y 2025), `alpha = 100` vuelve a ser el mejor (MAE medio 11,32), así que la elección no depende de un solo año. Dar más peso a los meses recientes, una tendencia propia por canal o añadir `lag_2` y la media de 3 meses no mejoran de forma clara (como mucho 11,18, un 1 %): se mantiene el modelo más sencillo.

**Prueba final (una sola vez):** MAE 16,14 unidades y WAPE 13,53 %. Empeora respecto a la validación, como es normal con datos nuevos, pero sigue por debajo de la referencia estacional en el mismo periodo (21,24). El modelo se queda corto de media en 14 unidades porque las ventas de 2026 crecen (119 unidades por serie y mes frente a 104 en 2025).

**Reentrenar con 2022–2025 (solo contexto):** con el mismo `alpha = 100` y 2025 incluido en el entrenamiento, el error en la prueba baja a 14,08 unidades (WAPE 11,80 %). No cambia la decisión: el test ya estaba abierto, así que la medida honesta sigue siendo 16,14. Antes de usar el modelo en producción conviene reentrenarlo con todo el histórico y medirlo con datos nuevos.

**Errores destacados:**
- Abril 2026, `ecommerce` + `urban` + `metro`: predice 230 y se venden 328. Salto de primavera mayor que en años anteriores.
- En los meses con rotura de stock el error es siempre por defecto: la venta registrada es igual al stock y la predicción no puede superarlo. La demanda real fue mayor de lo que se ve.

**Previsión de julio 2026 (no validada):** 2 398 unidades con 2 951 en stock. Fichero: `evidencies/prediccions_juliol_2026.csv`.

## 5. Segmentación de clientes

Variables: gasto anual y pedidos (en logaritmo), días desde el último pedido, ratio de devoluciones y antigüedad, estandarizadas. Se excluyen `customer_id`, `snapshot_date` y `avg_order_value` (repite gasto y pedidos). Técnica: K-Means; se elige k = 4 (silueta 0,24) porque cada grupo tiene lectura comercial. Con k = 2 la silueta es mayor, pero solo separa activos de inactivos.

| Segmento | Clientes | Perfil | Acción |
|---|---|---|---|
| Fieles veteranos | 650 | ~1 350 €, 6 pedidos, ~8 años de antigüedad | Programa de fidelidad |
| Nuevos activos | 644 | ~1 456 €, 6 pedidos, ~2,5 años | Bienvenida al segundo año |
| Ocasionales inactivos | 532 | ~216 €, 2 pedidos, casi 4 meses sin comprar | Reactivar con el servicio técnico |
| Devoluciones altas | 174 | ~369 €, devuelven el 40 % | Revisar las causas |

270 clientes (13,5 %) son fronterizos. Frente a la segmentación por reglas, K-Means separa a los clientes de valor alto que las reglas metían como o casionales y descubre el grupo de devoluciones.

## 6. Recomendaciones

1. **Stock (confianza media):** subir el stock de julio en `store` + `urban` + `inland`, `store` + `mountain` + `metro` y `store` + `electric` + `inland`, donde la previsión llega al stock. Añadir un margen de unas 14 unidades en `ecommerce` + `metro` y en `urban`.
2. **Campaña (confianza baja):** mantener `summer` y medir su efecto con una prueba por regiones, porque coincide con la temporada.
3. **Clientes:** fidelizar a los veteranos, reactivar a los ocasionales con el servicio técnico y revisar las devoluciones antes de actuar.

## 7. Limitaciones

- Datos sintéticos: una relación aprendida no demuestra una causa real.
- La censura por stock oculta la demanda no atendida.
- El modelo se queda corto cuando las ventas crecen más rápido que en el pasado.
- La previsión de julio no se puede validar con estos datos.
- La segmentación es una foto: no hay compras posteriores para comprobar si las acciones funcionan.

## 8. Reproducir

```bash
uv sync
uv run jupyter lab
```

Ejecutar en orden `notebooks/01_eda.ipynb`, `02_modelatge_baseline.ipynb` y `03_segmentacio.ipynb`. Después generar el panel:

```bash
uv run python src/panel.py
```

El panel queda en `evidencies/panel.html`.

## 9. Reparto del trabajo

| Miembro | Trabajo |
|---|---|
| Andy | Baseline por medias de grupo, notebook de métricas por campaña y región, cuaderno de seguimiento |
| Dennis | EDA, ficha del CP1, preparación y modelado (notebook 02), segmentación, panel y memoria |
| Guillem | *Pendiente de completar por el equipo* |
