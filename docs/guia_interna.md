# Guía interna · Entender lo que presentamos

Documento solo para el equipo. No se enseña en la defensa: sirve para que los tres entendamos cada cifra y cada decisión, y podamos responder preguntas de cualquier parte, no solo de la nuestra. El guion de lo que se dice está en `docs/defensa.md`; aquí está el porqué.

## 1. La historia en un minuto

1. BiciTierra tiene que decidir **cada mes cuánto stock** manda a cada canal y región.
2. Para eso queremos **predecir las bicis vendidas el mes que viene** en cada una de las 18 series.
3. Lo hacemos **sin trampas**: separamos los datos por fechas y solo usamos lo que se sabe antes de que empiece el mes.
4. Una **regresión ridge** se equivoca en 12,1 bicis por serie y mes, un **31 % menos** que la mejor referencia simple (17,4).
5. En la **prueba final** (enero–junio 2026) falla en 16,1 bicis: sigue ganando a la referencia (21,2), pero **se queda corto** porque en 2026 se vende más.
6. Para **julio de 2026** prevé 2 398 bicis; en **tres series de tienda** la previsión llega al stock, así que recomendamos subirlo.
7. Aparte, **K-Means** divide a los 2 000 clientes en **cuatro perfiles**, cada uno con una acción comercial.

Si alguien del tribunal se pierde, esta es la línea a la que hay que volver.

## 2. Vocabulario que hay que dominar

| Término | Qué es, en una frase | Ejemplo nuestro |
|---|---|---|
| **Serie** | Una combinación de canal × línea × región, seguida mes a mes | Online · urbanas · costa |
| **Fila** | Una serie en un mes concreto | Online · urbanas · costa · julio 2022 |
| **`lag_1` / `lag_12`** | Lo que vendió la misma serie hace 1 mes y hace 12 meses | Para julio 2022: junio 2022 y julio 2021 |
| **MAE** | Error medio en bicis, sin signo: cuánto nos equivocamos de media por serie y mes | 12,05 en validación |
| **WAPE** | Error total dividido entre ventas totales, en %. Permite comparar series grandes y pequeñas | 13,5 % en la prueba |
| **Sesgo** | Error medio **con** signo: si nos equivocamos siempre hacia el mismo lado | −14: nos quedamos cortos |
| **Fuga de información** | Usar para predecir algo que todavía no se conoce cuando se tiene que predecir | Usar `revenue` del mismo mes |
| **Censura por stock** | Si se agota el stock, la venta registrada es menor que la demanda real | 19 % de los meses |
| **Referencia (baseline)** | Un modelo muy simple con el que compararse | Repetir el mismo mes del año anterior |
| **Ridge** | Regresión lineal que castiga los pesos grandes (regularización) | Nuestro modelo |
| **`alpha`** | La fuerza de ese castigo: más alpha, pesos más pequeños | Elegimos 100 |
| **Pipeline** | Cadena de pasos de scikit-learn que se aplica siempre igual al entrenar y al predecir | Imputar → one-hot → escalar → ridge |
| **Imputar** | Rellenar los nulos | Con la mediana de entrenamiento |
| **One-hot** | Convertir una categoría en columnas de 0 y 1 | «online» → 1 en la columna online |
| **Escalar (z)** | Pasar cada valor a «cuántas desviaciones está de la media» | Presupuesto y descuento en la misma escala |
| **K-Means** | Agrupa los puntos que están cerca entre sí en k grupos | k = 4 perfiles |
| **Silueta** | De −1 a 1: cuánto se parece cada punto a su grupo frente al grupo vecino | 0,24 con k = 4 |
| **Inercia / codo** | Lo apretados que están los grupos; se busca el punto donde dejar de añadir grupos apenas mejora | Usado para elegir k |

**Cuidado con confundirlas:** MAE va en bicis; WAPE en porcentaje. Un WAPE del 13,5 % **no** significa que el modelo «acierte un 86,5 %»: significa que, sumando todos los errores, nos equivocamos en un 13,5 % de lo vendido.

## 3. Diapositiva a diapositiva

### 1 · Portada

Solo presentación. Lo importante es decir pronto que **los datos son sintéticos**: así ninguna conclusión se toma como una previsión real de mercado y nos cubrimos ante preguntas del tipo «¿esto pasa de verdad?».

### 2 · El problema

- **18 series** = 2 canales (tienda, online) × 3 líneas (urbana, montaña, eléctrica) × 3 regiones (costa, interior, metro).
- Las 18 gráficas tienen **la misma escala vertical** a propósito: así se ve qué series venden más. Si cada una tuviera su escala, todas parecerían igual de grandes.
- La condición **«solo lo que se sabe antes del mes»** es la clave de todo el proyecto: viene de la decisión de negocio (el stock se decide antes de vender) y luego justifica qué variables usamos.

### 3 · Los datos y su calidad

- **84 nulos en 5 columnas.** Tres de esas columnas (`marketing_spend`, `avg_discount`, `website_sessions`) no las usamos porque solo se conocen al cierre del mes, así que sus nulos no nos afectan. Las otras dos (`marketing_budget`, `planned_discount`) sí, y las rellenamos con la **mediana de entrenamiento**.
- **Por qué no con 0:** un 0 en presupuesto significa «este mes no se invirtió nada», y eso es una afirmación falsa. La mediana significa «un mes normal», que es lo más prudente cuando no sabemos.
- **Por qué la mediana y no la media:** la mediana no se mueve por unos pocos meses con presupuestos muy altos.
- **Por qué la mediana de entrenamiento:** si la calculáramos con todos los años, estaríamos usando información de 2025 y 2026 para preparar los datos de 2022. Es una fuga pequeña, pero fuga.
- **Mapa de calor:** una fila por serie, una columna por mes. Las franjas verticales que se repiten son la temporada. Con el botón «Roturas de stock» se ven los meses en que se agotó.
- **19 % de roturas:** en esos meses, la venta registrada = el stock disponible. La demanda real fue mayor, pero no sabemos cuánto. Por eso, en esos meses el modelo siempre falla por defecto.

### 4 · Hipótesis

- Se calculan **solo con 2021–2024** (el periodo de entrenamiento, más 2021 que sirve para los retrasos). Mirar 2025 o 2026 para plantear hipótesis sería espiar los datos de evaluación.
- **Montaña ×2,1:** media de julio frente a media de enero, en las ventas de montaña (unas 131 frente a 63).
- **Eléctricas +28 %:** ventas de 2024 frente a 2021.
- **Cómo se confirman:** la temporada, porque `lag_12` (ventas de hace un año) mejora mucho a la media plana; el crecimiento, porque los mayores errores del modelo en 2026 son precisamente crecimiento que no capta.
- **Límite:** la temporada de verano coincide con la campaña `summer`, así que no podemos separar el efecto de una y otra.

### 5 · Cómo evitamos hacer trampa

**Partición temporal:**

| Periodo | Para qué | Filas |
|---|---|---|
| 2021 | Solo para calcular `lag_12` de 2022 | — |
| 2022–2024 | Entrenar: el modelo aprende | 648 |
| 2025 | Validar: elegir entre modelos y alphas | 216 |
| Enero–junio 2026 | Probar **una sola vez** con el modelo ya elegido | 108 |
| Julio 2026 | Predecir: no hay venta real | 18 |

- **Por qué no al azar:** predecimos el futuro. Si mezclamos meses, el modelo entrena con marzo de 2025 y se evalúa en febrero de 2025, es decir, «ve el futuro». El error sale mejor de lo que será en la realidad.
- **Por qué tres trozos y no dos:** si eligiéramos el modelo mirando la prueba, la prueba dejaría de ser independiente. La validación sirve para elegir; la prueba, para medir honestamente.

**El botón «Hacer trampa con revenue»:** `revenue` = unidades × precio × (1 − descuento). Si se lo damos al modelo, solo tiene que deshacer esa cuenta, y el error baja a prácticamente 0. Parece perfecto, pero en la vida real los ingresos de julio no existen hasta que acaba julio. Es el ejemplo más claro de fuga de información y suele gustar al tribunal.

### 6 · Comparativa de modelos

| Modelo | MAE validación 2025 | Qué hace |
|---|---|---|
| Media de la serie | 18,75 | Predice siempre la media histórica de esa serie |
| Mismo mes del año anterior | 17,40 | Predice `lag_12` |
| Ridge α = 1 | 12,43 | Regresión con todas las variables admitidas |
| Ridge α = 10 | 12,37 | Igual, con más castigo |
| **Ridge α = 100** | **12,05** | **El elegido** |

- **Mejora del 31 %:** 1 − 12,05 / 17,40 ≈ 0,31. Se compara con la **mejor** referencia, no con la peor, para no inflar la mejora.
- **Por qué empezar con referencias:** un MAE de 12 no dice nada por sí solo. Comparado con 17,4, dice que el modelo aporta.
- **La elección es estable:** los tres alphas dan entre 12,05 y 12,43. Si hubiera una diferencia enorme entre ellos, sospecharíamos de suerte.
- **Validación cruzada temporal:** entrenamos con el pasado y validamos 2023, después 2024 y después 2025. Alpha 100 gana también en la media (11,32). Así no dependemos de un solo año.
- **Lo que probamos y no usamos:** dar más peso a los meses recientes, tendencia propia por canal, `lag_2` y media de 3 meses. Ninguna mejora más de un 1 %, así que nos quedamos con lo más sencillo. Esto demuestra que buscamos mejoras y las descartamos con criterio.

### 7 · Prueba final

- **16,14 bicis de MAE y 13,53 % de WAPE**, frente a 21,24 de la referencia en el mismo periodo.
- **Por qué empeora respecto a 2025:** la validación se usó para elegir (y por eso favorece un poco al modelo), y además 2026 crece: 119 bicis por serie y mes frente a 104 en 2025.
- **Sesgo de −14:** el error no es aleatorio; casi siempre predecimos de menos. La gráfica de real frente a previsto lo enseña: la línea prevista va por debajo todos los meses.
- **Peor caso:** abril 2026, online · urbanas · metro. Previsto 230, real 328. Fue un salto de primavera mayor que en años anteriores.
- **Una sola vez:** después de ver la prueba no se cambió nada. Si se pregunta, la respuesta es un «no» rotundo.
- **Dato de contexto (solo si preguntan):** reentrenando con 2022–2025, el error en la prueba bajaría a 14,08. No lo presentamos como resultado porque el test ya estaba abierto.

### 8 · Puesta en marcha (el Pipeline)

El modelo del notebook 02 está montado en `src/modelo.py` como Pipeline de scikit-learn. La diapositiva sigue **una fila real**: online · urbanas · costa · julio 2022, que tiene el presupuesto vacío.

| Paso | Qué entra | Qué sale | Por qué |
|---|---|---|---|
| 1 · Separar | Una fila del CSV con todo | X (lo de antes del mes) e y (`sales_units`) | Lo que solo se sabe al cierre se queda fuera |
| 2 · `SimpleImputer` | Presupuesto vacío | Unos 2 800 € (mediana de 2022–2024) | Un nulo no es un 0 |
| 3 · `OneHotEncoder` | Canal, línea, región, campaña (texto) | 13 columnas de 0 y 1 | Un modelo lineal solo multiplica números |
| 4 · `StandardScaler` | Cada columna en sus unidades | Todas en «desviaciones respecto a la media» | Que los euros no dominen por ser números grandes |
| 5 · `Ridge(alpha=100)` | 648 filas × 29 columnas | Un peso por columna | Aprende cuánto sube o baja cada variable |
| 6 · `.predict()` | Nuestra fila | 176 bicis (real: 210) | Media + suma de aportes |
| 7 · `joblib` | El Pipeline entrenado | Un archivo de 5 KB | Para julio se carga y se predice, sin reentrenar |

**29 columnas** = 16 numéricas (presupuesto, descuento, stock, precio, días del mes, `lag_1`, `lag_12`, temporada con seno y coseno, tendencia y la temporada propia de cada línea) + 13 de one-hot (2 canales + 3 líneas + 3 regiones + 5 campañas).

**Cómo sale el 176** (la cuenta que enseña la diapositiva):

| Parte | Bicis |
|---|---|
| Media de entrenamiento (β₀) | 98,6 |
| Stock inicial | +21,9 |
| Ventas del mes anterior | +8,3 |
| Línea urbana | +7,9 |
| Ventas de hace un año | +7,7 |
| Campaña de verano | +7,0 |
| Resto de columnas | +24,9 |
| **Previsión** | **≈ 176** |

Como todas las columnas están escaladas, β₀ coincide con la media de ventas del entrenamiento, y cada aporte es «peso × valor escalado». Esa fila vendió 210 con 218 en stock: se quedó con 8 bicis, casi una rotura.

**El recorrido de alpha:** con α = 1, 10 o 100 el error ronda 12; con 1 000 sube a 13,3 y con 10 000 se dispara a 24,1. Con tanto castigo los pesos se aplastan hacia 0 y el modelo acaba prediciendo casi la media para todo (subajuste).

**Por qué la temporada con seno y coseno:** si usáramos el mes como número (1 a 12), diciembre (12) y enero (1) quedarían muy lejos, cuando en realidad están juntos. Con seno y coseno el año es un círculo.

### 9 · Julio y recomendación de stock

- **2 398 bicis previstas con 2 951 en stock.** Las predicciones se recortan entre 0 y el stock (`np.clip`), porque no se puede vender más de lo que hay.
- **Las tres series que llegan al stock:** tienda · urbanas · interior, tienda · montaña · metro y tienda · eléctricas · interior.
- **El simulador** recalcula la previsión con la fórmula del ridge: base + efecto de cada variable × cambio, y luego recorta con el stock.

| Stock | Total previsto | Series al límite |
|---|---|---|
| Sin cambios | 2 398 | 3 |
| +5 % | 2 441 | 2 (sale urbanas · interior) |
| +35 % | 2 679 | 1 (queda eléctricas · interior) |
| +40 % | 2 713 | 0 |

- **La trampa del simulador:** al subir el stock sube la previsión **en las 18 series**, porque el modelo ha aprendido unas 0,23 bicis más por cada bici de stock. Eso **no** quiere decir que poner stock haga vender. Quiere decir que la empresa ya pone más stock donde espera vender más (y que, con poco stock, se vende menos porque se agota). Es una relación, no una causa. El stock es la variable con más peso del modelo, así que esta pregunta es muy probable.
- **El margen de 14 bicis** en online · metro y en urbanas viene del sesgo de la prueba: si sabemos que nos quedamos cortos unas 14 bicis, lo prudente es cubrirlo.
- **Confianza media:** el modelo gana a la referencia, pero en 2026 ha fallado por defecto y julio no se puede validar.

### 10 · Clientes

- **Cinco variables:** gasto anual y pedidos (en logaritmo, para que unos pocos clientes muy grandes no dominen), días desde el último pedido, ratio de devoluciones y antigüedad. Todas **escaladas**, porque K-Means mide distancias y, sin escalar, los euros mandarían sobre todo.
- **Excluidas:** `customer_id` (es un número de identificación, no un comportamiento), `snapshot_date` (es igual para todos) y `avg_order_value` (gasto = ticket × pedidos: estaríamos contando dos veces lo mismo).
- **Nulos:** 30 clientes sin gasto, reconstruido como ticket × pedidos; 20 sin fecha del último pedido, rellenados con la mediana.

| Perfil | Clientes | Gasto anual | Pedidos | Días sin comprar | Antigüedad | Acción |
|---|---|---|---|---|---|---|
| Fieles veteranos | 650 | ~1 350 € | 6 | ~30 | ~7,7 años | Fidelizar |
| Nuevos activos | 644 | ~1 456 € | 6 | ~33 | ~2,6 años | Bienvenida al segundo año |
| Ocasionales inactivos | 532 | ~216 € | 2 | ~114 | ~5 años | Reactivar con el servicio técnico |
| Devoluciones altas | 174 | ~369 € | 3 | ~53 | ~5,5 años | Revisar por qué devuelven |

- **Por qué k = 4:** con k = 2 la silueta es mayor, pero solo separa activos de inactivos, cosa que ya hacían las reglas sencillas. Con 4, la inercia baja de forma clara, la silueta (0,24) mejora frente a k = 3 y cada grupo tiene una acción distinta. La elección mezcla criterio técnico y utilidad para el negocio, y hay que decirlo así.
- **Silueta 0,24:** es baja-moderada; los grupos existen pero se tocan. 270 clientes (13,5 %) son fronterizos. Es honesto reconocerlo.
- **Qué aporta frente a las reglas:** K-Means separa a clientes de valor alto que las reglas metían como ocasionales y descubre el grupo de devoluciones, que ninguna regla buscaba.

### 11 · Demo de clientes

- **Ejes:** vertical, gasto anual en escala logarítmica (cada salto de línea multiplica, no suma); horizontal, días desde el último pedido.
- **1 980 puntos**, no 2 000: los 20 sin fecha del último pedido no se pueden dibujar en el eje horizontal.
- **Lo que hay que hacer ver:** fieles y nuevos activos ocupan la misma zona; los separa la antigüedad, que no está en el gráfico. Los de devoluciones altas quedan en medio, mezclados. Es decir, **dos ejes no bastan**: por eso el clustering usa cinco variables.

### 12 · Límites y cierre

Los cuatro límites y lo que hay detrás de cada uno:

1. **Datos sintéticos:** una relación aprendida no demuestra una causa. Vale también para el stock y las campañas.
2. **Censura por stock:** en el 19 % de los meses no vemos la demanda real.
3. **Se queda corto cuando las ventas crecen:** sesgo de −14 en 2026.
4. **Julio no se puede validar:** no hay venta real.

Decir los límites nosotros antes de que nos los pregunten da credibilidad.

## 4. Las cifras de memoria

| Cifra | Qué es | De dónde sale |
|---|---|---|
| 66 meses · 18 series · 2 000 clientes | Tamaño de los datos | `data/originales/` |
| 84 nulos en 5 columnas | Calidad del histórico | `sales_history.csv` |
| 19 % | Meses con rotura de stock | Columna `stockout` |
| ×2,1 · +28 % | Temporada de montaña · crecimiento de eléctricas | Notebook 01, solo 2021–2024 |
| 18,75 · 17,40 · 12,05 | MAE de las dos referencias y del modelo (2025) | `evidencies/metricas_modelos.csv` |
| 31 % | Mejora frente a la mejor referencia | 1 − 12,05 / 17,40 |
| 11,32 | MAE medio en validación cruzada temporal | Notebook 02 |
| 16,14 · 13,53 % · 21,24 | MAE, WAPE y referencia en la prueba | `metricas_modelos.csv` |
| −14 | Sesgo en la prueba | `prediccions_prova_2026.csv` |
| 230 frente a 328 | Peor caso (abril, online, urbanas, metro) | `prediccions_prova_2026.csv` |
| 648 filas · 29 columnas · 5 KB | Entrenamiento del Pipeline | `src/modelo.py` |
| 2 398 de 2 951 | Previsión y stock de julio | `prediccions_juliol_2026.csv` |
| 650 · 644 · 532 · 174 | Clientes por perfil | `perfil_segmentos.csv` |
| 0,24 | Silueta con k = 4 | Notebook 03 |

## 5. Frases que no hay que decir

| No digáis | Decid | Por qué |
|---|---|---|
| «El modelo acierta un 86 %» | «Nos equivocamos en un 13,5 % de lo vendido» | El WAPE no es una tasa de acierto |
| «Si ponemos más stock, venderemos más» | «Donde hay más stock se vende más; es una relación» | El stock es una decisión de la empresa, no una causa demostrada |
| «En julio venderemos 2 398» | «Prevemos 2 398» | Julio no se ha validado |
| «K-Means encuentra los grupos reales» | «K-Means propone cuatro grupos útiles» | Con silueta 0,24 los grupos se tocan; k lo elegimos nosotros |
| «Alpha es la velocidad de aprendizaje» | «Alpha es cuánto se castigan los pesos grandes» | Ridge no aprende por pasos; alpha regulariza |
| «Probamos varias veces la prueba» | «La prueba se ejecutó una sola vez» | Es la base de que el 16,1 sea honesto |
| «La campaña de verano funciona» | «La campaña coincide con la temporada; no podemos separarlas» | Habría que medirlo con una prueba por regiones |

## 6. Cómo se genera todo

```bash
uv sync                                   # instalar el entorno
uv run python src/modelo.py entrenar      # entrena, comprueba que coincide con el notebook 02 y guarda el modelo
uv run python src/modelo.py predecir      # carga el modelo y predice julio
uv run python src/panel.py                # genera evidencies/panel.html
uv run python src/presentacion.py         # genera evidencies/presentacion.html con las notas de docs/defensa.md
```

- `src/modelo.py entrenar` tiene una comprobación: si el MAE del Pipeline se aleja más de 0,1 del notebook 02, se para. Así sabemos que la diapositiva 8 enseña exactamente el modelo que hemos evaluado.
- Las notas del presentador (tecla N) salen de `docs/defensa.md`. Si se cambia el guion, hay que volver a ejecutar `src/presentacion.py`.
