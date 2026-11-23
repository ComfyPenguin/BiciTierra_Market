# Defensa · BiciTierra Market

Duración objetivo: **9 minutos** (máximo 10). Cada miembro presenta un bloque y todos deben poder responder preguntas de cualquier parte.

## Reparto propuesto

| Bloque | Diapositivas | Quién | Tiempo |
|---|---|---|---|
| Problema, datos e hipótesis | 1–4 | Andy | 2:30 |
| Modelo de ventas | 5–8 | Dennis | 3:30 |
| Clientes, panel y cierre | 9–11 | Guillem | 3:00 |

## Guion por diapositiva

**1 · Portada (0:15).** «Somos Andy, Guillem y Dennis. Os presentamos cómo BiciTierra puede anticipar sus ventas mensuales y conocer mejor a sus clientes. Los datos son sintéticos.»

**2 · El problema (0:45).** «La dirección tiene que decidir cada mes cuánto stock poner en cada canal y región. Nuestra pregunta: ¿cuántas bicis venderemos el mes siguiente en cada una de las 18 combinaciones de canal, producto y región, usando solo lo que sabemos antes de que empiece el mes? Y como segunda pregunta: ¿qué tipos de clientes hay y qué hacemos con cada uno?»

**3 · Los datos y su calidad (0:45).** «Tenemos 66 meses de 18 series y 2 000 clientes. Dos problemas importantes. Uno: hay nulos, y un nulo no es un cero; rellenarlos con 0 diría que no hubo presupuesto. Dos: en el 19 % de los meses se agota el stock, así que la venta registrada es menor que la demanda real y no vemos cuánto más se habría vendido.»

**4 · Hipótesis (0:45).** «Del periodo de entrenamiento sacamos dos hipótesis. Primera: las ventas tienen temporada; en julio las de montaña doblan las de enero. Segunda: las eléctricas y la venta online crecen, un 28 % las eléctricas en cuatro años. Las dos se confirman después en el modelo.»

**5 · Cómo evitamos hacer trampa (0:50).** «Separamos por fechas: aprendemos con 2022–2024, elegimos el modelo con 2025 y dejamos 2026 para una sola prueba final. Y solo usamos variables que se conocen antes del mes. Un ejemplo: si usáramos los ingresos del mes, reconstruiríamos las ventas con error cero. Parece perfecto, pero es imposible de aplicar, porque los ingresos de julio no se conocen hasta que acaba julio.»

**6 · Comparativa de modelos (0:50).** «Primero, dos referencias simples: la media de cada serie falla en 18,8 bicis por serie y mes, y repetir el mismo mes del año anterior falla en 17,4. Después, una regresión ridge con todas las variables admitidas baja a 12,1. Elegimos ridge con alpha 100: un 31 % menos de error, y los tres valores de alpha daban casi lo mismo, así que la elección es estable. Lo comprobamos validando también 2023 y 2024: alpha 100 vuelve a ganar.»

**7 · Prueba final (0:50).** «Con el modelo congelado, lo probamos una sola vez en enero–junio de 2026: 16,1 bicis de error, un 13,5 %. Empeora respecto a 2025, que es lo normal con datos nuevos, pero sigue por debajo de la referencia. El fallo principal es que se queda corto, unas 14 bicis de media, porque en 2026 se vende más. El peor caso: abril, online, urbanas, región metro; predijimos 230 y se vendieron 328.»

**8 · Julio y recomendación de stock (0:50).** «Para julio prevemos 2 398 bicis. Es una previsión, no un resultado: no tenemos la venta real. En tres series de tienda física la previsión llega al stock disponible, así que recomendamos subir su stock. Y como el modelo se queda corto, añadir un margen en online-metro y en urbanas. Confianza media.»

**9 · Clientes (1:00).** «Agrupamos los clientes con K-Means usando gasto, pedidos, días sin comprar, devoluciones y antigüedad. Salen cuatro perfiles: fieles veteranos y nuevos activos, que gastan unos 1 400 € al año; ocasionales inactivos, con unos 200 € y casi cuatro meses sin comprar; y un grupo pequeño que devuelve el 40 % de lo que compra. Para cada uno, una acción: fidelizar, dar la bienvenida al segundo año, reactivar con el servicio técnico y revisar las causas de las devoluciones.»

**10 · Demo del panel (1:15).** Abrir `evidencies/panel.html`. Señalar, por este orden: los indicadores de arriba; la gráfica mensual con la temporada y la previsión de julio en discontinua; la comparativa de modelos; la tabla de julio con las tres series en rojo; la tabla de segmentos.

**11 · Límites y cierre (0:45).** «Límites: datos sintéticos, así que una relación no demuestra una causa; la rotura de stock oculta demanda; el modelo se queda corto cuando las ventas crecen; y julio no se puede validar todavía. En resumen: un modelo sencillo y honesto que mejora un 31 % a la referencia, una recomendación de stock concreta y cuatro perfiles de cliente con acción. Gracias.»

## Preguntas probables

**¿Por qué no hicisteis una partición aleatoria?**
Porque predecimos el futuro. Con una partición aleatoria, el modelo aprendería de meses posteriores al que predice y el error saldría más bajo de lo real.

**¿Por qué no usasteis `revenue` o `website_sessions`?**
Se conocen al cierre del mes. Además, `revenue` contiene las propias unidades: con él el error sale 0, que es una fuga de información.

**¿Qué es MAE y qué es WAPE?**
MAE: cuántas bicis nos equivocamos de media por serie y mes. WAPE: el error total dividido por las ventas totales, en porcentaje; sirve para comparar series grandes y pequeñas.

**¿Por qué el error de la prueba es peor que el de validación?**
Es lo esperable: la validación se usó para elegir y la prueba son meses que el modelo nunca vio. Además, en 2026 las ventas crecen y el modelo se queda corto.

**¿Habéis cambiado algo después de ver la prueba?**
No. El modelo y sus parámetros se dejaron escritos antes de abrir 2026, y la prueba se ejecutó una sola vez.

**¿Qué hace la regularización?**
Castiga los coeficientes grandes para que el modelo no se ajuste de más a los años de entrenamiento. `alpha` controla cuánto se castiga.

**¿Por qué `stock_units` es la variable con más peso? ¿Poner más stock vende más?**
No necesariamente. Las ventas están limitadas por el stock, y la empresa ya pone más stock donde espera vender más. Es una relación, no una causa.

**¿Por qué cuatro grupos y no dos, si dos tienen mejor silueta?**
Con dos solo separamos activos de inactivos, que ya lo hacían las reglas. Con cuatro, la inercia baja de forma clara, la silueta mejora respecto a tres y cada grupo tiene una acción distinta.

**¿Por qué no usasteis `avg_order_value` en el clustering?**
Porque el gasto es ticket × pedidos. Con las tres variables contaríamos dos veces el mismo comportamiento.

**¿Por qué escalasteis las variables?**
K-Means mide distancias. Sin escalar, la variable en euros dominaría a la de días o a la de devoluciones.

**¿La previsión de julio es fiable?**
Es una previsión, no un resultado validado. Por el error de la prueba, esperamos fallar unas 16 bicis por serie, casi siempre por defecto.

**¿`alpha = 100` no es casualidad de 2025?**
No. Con validación cruzada temporal (validando 2023, 2024 y 2025, siempre entrenando con el pasado) también gana `alpha = 100`, con 11,32 bicis de error medio.

**¿Probasteis a dar más peso a lo reciente?**
Sí: pesos que bajan con la antigüedad, tendencia propia por canal y más retrasos. Ninguna mejora más de un 1 %, así que nos quedamos con el modelo más sencillo.

**¿Qué mejoraríais?**
Reentrenar con todo el histórico antes de predecir: con 2025 incluido el error de la prueba baja de 16,1 a 14,1 (solo como contexto, porque el test ya estaba abierto). También tratar la censura por stock y medir el efecto real de las campañas con una prueba.

## Comprobación antes de la defensa

- [ ] Los tres notebooks se ejecutan de arriba abajo sin errores.
- [ ] `uv run python src/panel.py` genera el panel y se abre en el portátil de la defensa.
- [ ] Cada miembro sabe explicar: la pregunta, la clave de una fila, entrenamiento / validación / prueba, por qué no usar `revenue` y un perfil de cliente.
- [ ] Autoevaluación rellenada.
- [ ] Ensayo cronometrado por debajo de 10 minutos.
