# Defensa · BiciTierra Market

Duración objetivo: **17 minutos y medio** (rango permitido: 15–20). Si vais justos de tiempo, acortad las demos (diapositivas 5, 8, 9 y 11), nunca las explicaciones. Cada miembro presenta un bloque y todos deben poder responder preguntas de cualquier parte.

Convención del guion: lo que va entre «comillas» se dice; lo que va entre [corchetes] se hace en la pantalla.

## Reparto propuesto

| Bloque | Diapositivas | Quién | Tiempo |
|---|---|---|---|
| Problema, datos e hipótesis | 1–4 | Andy | 4:45 |
| Modelo de ventas | 5–9 | Dennis | 8:30 |
| Clientes, demo y cierre | 10–12 | Guillem | 4:15 |

## Hoja de ruta

**El hilo en una frase:** queremos saber cuántas bicis venderemos el mes que viene → lo medimos sin hacer trampa → un modelo sencillo mejora un 31 % a la referencia, aunque se queda corto cuando las ventas crecen → con él recomendamos stock para julio → y los clientes se dividen en cuatro perfiles con una acción cada uno.

| # | Empieza en | Quién | Idea que el tribunal se tiene que llevar | Qué se toca en pantalla | Puente a la siguiente |
|---|---|---|---|---|---|
| 1 | 0:00 | Andy | Quiénes somos, las dos preguntas y que los datos son sintéticos | Nada | «Empecemos por el problema.» |
| 2 | 0:45 | Andy | 18 series y solo vale lo que se sabe antes del mes | Señalar las 18 gráficas | «Antes de modelar, miramos los datos.» |
| 3 | 2:00 | Andy | Dos trampas: un nulo no es un cero y la rotura de stock esconde demanda | Botón «Roturas de stock» | «Con los datos limpios, planteamos hipótesis.» |
| 4 | 3:30 | Andy | Hay temporada y las eléctricas crecen | Señalar la línea de montaña | «Dennis os explica cómo lo construimos.» |
| 5 | 4:45 | Dennis | Separar por fechas y no usar lo que solo se sabe al cierre | Botón «Hacer trampa con revenue» | «Sin trampas, ¿qué modelo gana?» |
| 6 | 6:30 | Dennis | Ridge con alpha 100 mejora un 31 % a la mejor referencia | Señalar las barras | «Lo probamos una sola vez con meses nuevos.» |
| 7 | 8:00 | Dennis | En 2026 sigue ganando, pero se queda corto unas 14 bicis | Señalar real frente a previsto y el peor caso | «Así funciona por dentro.» |
| 8 | 9:30 | Dennis | Qué hace cada paso del Pipeline con una fila real | Flecha dos veces por paso (o ▶ Entrenar) | «Y ahora lo usamos para julio.» |
| 9 | 11:30 | Dennis | 2 398 bicis previstas, tres series se quedan sin stock | Deslizador de stock a +40 % y «Volver a la previsión» | «Guillem os cuenta los clientes.» |
| 10 | 13:15 | Guillem | Cuatro perfiles, cuatro acciones | Señalar cada tarjeta | «Veámoslo cliente a cliente.» |
| 11 | 15:00 | Guillem | Los grupos se ven en el gráfico y algunos solo se separan con más variables | Filtros por grupo y pasar el ratón por un punto | «Para acabar, los límites.» |
| 12 | 16:30 | Guillem | Límites honestos y tres resultados | Nada | «Muchas gracias. ¿Preguntas?» |

**Controles de tiempo** (la tecla N enseña el reloj y el tiempo de cada diapositiva):

- **A los 5 minutos** tiene que estar hablando Dennis. Si Andy va tarde, en la diapositiva 3 se puede saltar el botón de roturas y solo decirlo.
- **A los 10 minutos** se tiene que estar en la diapositiva 8. Si vais tarde, pulsad ▶ Entrenar y contad solo los pasos 2, 5 y 6.
- **A los 13 minutos y medio** tiene que estar hablando Guillem. Si vais tarde, en la diapositiva 11 basta con dos filtros: fieles e inactivos.
- **Si vais rápido** (menos de 15 minutos), alargad las demos: en la 9, mover también el presupuesto; en la 11, pasar el ratón por varios clientes.

**Si algo falla:** la presentación es un único archivo y funciona sin internet. Si una demo se queda colgada, F5 recarga y la URL vuelve a la misma diapositiva. Si el portátil falla, el panel `evidencies/panel.html` tiene las mismas cifras.

## Guion por diapositiva

**1 · Portada (0:45).** «Buenos días. Somos Andy, Guillem y Dennis, y os presentamos BiciTierra Market. BiciTierra es una cadena que vende bicis urbanas, de montaña y eléctricas en tienda física y online. Nuestro trabajo responde a dos preguntas: cuántas bicis va a vender el mes que viene y qué tipos de clientes tiene. Un aviso desde el principio: los datos son sintéticos, de enero de 2021 a junio de 2026. Yo os cuento el problema y los datos, Dennis el modelo de ventas y Guillem los clientes.»

**2 · El problema (1:15).** «Cada mes, la dirección tiene que decidir cuánto stock manda a cada sitio. Si se pasa, tiene bicis paradas en el almacén; si se queda corta, pierde ventas. Por eso nuestra pregunta principal es: ¿cuántas bicis venderemos el mes que viene en cada serie? Una serie es una combinación de canal, línea y región: dos canales, tres líneas y tres regiones dan 18 series. [Señalar las 18 gráficas pequeñas.] Aquí están las 18, todas con la misma escala vertical para poder compararlas. Ya se ve que no se parecen: unas venden mucho más que otras y casi todas suben y bajan a lo largo del año. Y hay una condición importante: solo podemos usar lo que se sabe antes de que empiece el mes, porque es cuando hay que decidir. La segunda pregunta es sobre clientes: ¿qué perfiles tenemos y qué acción conviene con cada uno?»

**3 · Los datos y su calidad (1:30).** «Trabajamos con 66 meses de esas 18 series y con 2 000 clientes. Al explorarlos encontramos dos trampas. La primera: hay 84 valores nulos repartidos en 5 columnas, por ejemplo el presupuesto de marketing. Un nulo no es un cero: si rellenáramos con 0, le diríamos al modelo que ese mes no hubo presupuesto, y eso es falso; simplemente no se registró. [Señalar el mapa de calor.] Este mapa tiene una fila por serie y una columna por mes, y el color indica las unidades vendidas, según la leyenda. Se ven las franjas de temporada repitiéndose cada año. [Pulsar «Roturas de stock».] La segunda trampa: en el 19 % de los meses se agotó el stock. Eso significa que la venta registrada es menor que la demanda real: si no quedan bicis, nadie puede comprarlas, y no sabemos cuántas más se habrían vendido. Lo tendremos en cuenta al interpretar el modelo.»

**4 · Hipótesis (1:15).** «Antes de modelar, planteamos hipótesis mirando solo los años de entrenamiento, de 2021 a 2024, para no espiar los datos con los que luego evaluamos. Primera hipótesis: las ventas tienen temporada. En julio, las de montaña venden 2,1 veces lo de enero. [Señalar la línea de montaña en la gráfica.] Se ve el pico cada verano. Segunda hipótesis: las eléctricas crecen; en 2024 vendieron un 28 % más que en 2021. Estas dos ideas nos dicen qué tiene que saber el modelo: en qué mes estamos y cuánto se vendió hace poco y hace un año. Y las dos se confirman después en el modelo. Ahora Dennis os explica cómo lo construimos.»

**5 · Cómo evitamos hacer trampa (1:45).** «Gracias, Andy. Lo más importante de un modelo de previsión es no hacer trampa sin darse cuenta. Hicimos dos cosas. Primera: separar por fechas, no al azar. [Señalar la línea de tiempo.] 2021 solo sirve para calcular las ventas de hace un año; aprendemos con 2022 a 2024; elegimos el modelo con 2025, y enero a junio de 2026 lo guardamos para una única prueba final. Si mezcláramos meses al azar, el modelo aprendería del futuro y el error saldría mejor de lo que es. Segunda: solo usamos variables que se conocen antes del mes. [Señalar las dos tarjetas.] A la izquierda, lo que sí sabemos: stock inicial, presupuesto aprobado, descuento previsto, precio, campaña, y las ventas del mes anterior y de hace un año. A la derecha, lo que solo se sabe al cerrar el mes, como los ingresos o las sesiones web. ¿Qué pasa si usamos los ingresos? [Pulsar «Hacer trampa con revenue».] El error baja a cero. Parece el modelo perfecto, pero es una fuga de información: los ingresos son unidades por precio, así que el modelo solo está deshaciendo una multiplicación. Y en la práctica es imposible, porque los ingresos de julio no se conocen hasta que acaba julio.»

**6 · Comparativa de modelos (1:30).** «Para saber si un modelo es bueno necesitamos con qué compararlo. Empezamos con dos referencias muy simples. La primera predice la media histórica de cada serie y se equivoca en 18,8 bicis por serie y mes. La segunda repite lo que se vendió el mismo mes del año anterior y falla en 17,4. Esta medida es el MAE: cuántas bicis nos equivocamos de media. Después probamos una regresión ridge, que es una regresión lineal con regularización: castiga los coeficientes grandes para que el modelo no se aprenda de memoria los años de entrenamiento. Probamos tres valores de alpha, que es la fuerza de ese castigo. [Señalar las barras.] Ridge con alpha 100 baja a 12,1 bicis: un 31 % menos de error que la mejor referencia. Además, los tres alphas dan casi lo mismo, de 12,1 a 12,4, así que la elección no depende de un detalle. Y para comprobar que no era suerte de 2025, validamos también 2023 y 2024, y alpha 100 vuelve a ganar.»

**7 · Prueba final (1:30).** «Con el modelo ya elegido y congelado, lo probamos una sola vez en enero a junio de 2026, meses que nunca había visto. Resultado: 16,1 bicis de error por serie y mes, un 13,5 % sobre el total vendido. La referencia, en el mismo periodo, falla en 21,2, así que el modelo sigue ganando. Que el error suba respecto a 2025 es lo normal: 2025 lo usamos para elegir y 2026 es completamente nuevo. [Señalar la gráfica de real frente a previsto.] Pero hay un patrón claro: la línea prevista va siempre por debajo de la real. En 2026 se vende más que en años anteriores y el modelo se queda corto, unas 14 bicis de media. [Señalar el peor caso.] El peor caso es abril, online, urbanas, región metro: predijimos 230 y se vendieron 328, casi 100 bicis de diferencia. Esto lo reconocemos como límite y lo tenemos en cuenta en la recomendación.»

**8 · Puesta en marcha (2:00).** «Ahora os enseñamos qué hace scikit-learn por dentro. Vamos a seguir una sola fila: online, urbanas, costa, julio de 2022, que además tiene el presupuesto vacío. Cada paso se ve en dos pulsaciones: primero cómo llegan los datos y después qué hace el paso.» [→ → paso 1.] «Separamos la fila: lo que se sabe antes del mes es X, las ventas son y, lo que queremos predecir, y los ingresos y el stock final se quedan fuera.» [→ → paso 2.] «El modelo es un Pipeline, una cadena de pasos que siempre se aplican en el mismo orden. SimpleImputer rellena el presupuesto que falta con la mediana del entrenamiento, unos 2 800 euros: un mes normal, no un mes sin presupuesto.» [→ → paso 3.] «OneHotEncoder convierte canal, línea, región y campaña en columnas de ceros y unos, porque un modelo lineal solo sabe multiplicar números.» [→ → paso 4.] «StandardScaler pone todas las columnas en la misma escala, para que los euros no pesen más que los días solo por ser números grandes.» [→ → paso 5.] «Ridge aprende un peso para cada una de las 29 columnas a partir de 648 filas. Si subimos alpha a 10 000, los pesos se aplastan hacia cero y el error se dispara a 24 bicis: el modelo deja de aprender.» [→ → paso 6.] «La previsión es la media de entrenamiento, unas 99 bicis, más lo que aporta cada columna: el stock, las ventas del mes anterior, que sea urbana, las de hace un año y la campaña de verano. Sale 176 y se vendieron 210.» [→ → paso 7.] «Todo se guarda en un archivo de 5 KB, y para julio solo se carga y se predice, sin volver a entrenar.» [Si vais tarde: pulsar ▶ Entrenar y contarlo mientras se reproduce.]

**9 · Julio y recomendación de stock (1:45).** «Con ese modelo predecimos julio de 2026: 2 398 bicis, con 2 951 en stock. Es una previsión, no un resultado: la venta real de julio todavía no existe.» [Señalar las tres barras en rojo.] «El total parece cómodo, pero en tres series de tienda física la previsión llega al stock disponible: urbanas de interior, montaña de metro y eléctricas de interior. Ahí la venta queda limitada por el stock.» [Subir el deslizador de stock hasta +40 %.] «Con un 40 % más de stock, ninguna serie llega al límite. Pero fijaos en el total: sube a unas 2 700 bicis, y sube en las 18 series, no solo en las tres. Eso no significa que poner más stock haga vender más. El modelo ha aprendido que la empresa pone más stock donde espera vender más: es una relación, no una causa.» [Pulsar «Volver a la previsión».] «Nuestra recomendación: subir el stock en esas tres series y, como sabemos que el modelo se queda corto, añadir un margen de unas 14 bicis en online-metro y en urbanas. Confianza media. Ahora Guillem os cuenta la parte de clientes.»

**10 · Clientes (1:45).** «Gracias, Dennis. La segunda pregunta era qué tipos de clientes tenemos. Usamos K-Means, que agrupa a los clientes que se parecen entre sí. Usamos cinco variables: gasto anual, pedidos, días desde la última compra, porcentaje de devoluciones y antigüedad. Las escalamos antes, porque K-Means mide distancias y sin escalar el gasto en euros mandaría sobre todo lo demás. Elegimos cuatro grupos porque cada uno tiene una acción distinta. [Señalar cada tarjeta.] Fieles veteranos: 650 clientes, gastan unos 1 350 euros al año y su última compra fue hace un mes; la acción es fidelizarlos. Nuevos activos: 644 clientes, gastan aún más, unos 1 450, pero llevan poco; hay que darles la bienvenida al segundo año para que no se vayan. Ocasionales inactivos: 532 clientes, unos 200 euros y casi cuatro meses sin comprar; los reactivaríamos con el servicio técnico, por ejemplo una revisión de la bici. Y un grupo pequeño, 174 clientes, que devuelve el 40 % de lo que compra; ahí no toca vender más, sino revisar por qué devuelven.»

**11 · Demo de clientes (1:30).** «Cada punto es un cliente.» [Señalar los ejes.] «Hacia arriba, cuánto gasta, en escala logarítmica; hacia la derecha, cuántos días hace que no compra. Son 1 980 clientes: los otros 20 no tienen fecha de última compra.» [Pulsar «Fieles veteranos».] «Los fieles están arriba a la izquierda: gastan mucho y compraron hace poco.» [Pulsar «Nuevos activos».] «Los nuevos activos están en la misma zona. Lo que los separa de los fieles no se ve aquí: es la antigüedad, unos dos años y medio frente a casi ocho.» [Pulsar «Ocasionales inactivos».] «Los inactivos, abajo y a la derecha: gastan poco y hace meses que no vienen.» [Pulsar «Devoluciones altas».] «Y los de devoluciones altas quedan en medio, mezclados con los demás: los distingue una variable que aquí no se ve. Por eso hace falta el clustering con las cinco variables y no basta una regla con dos ejes.» [Pasar el ratón por un punto y pulsar «Todos».] «Cada punto muestra sus datos. Y todo esto está también en el panel completo, que entregamos aparte.»

**12 · Límites y cierre (1:00).** «Para acabar, los límites, porque un resultado sin límites no es honesto. Uno: los datos son sintéticos, y además una relación no demuestra una causa. Dos: la rotura de stock oculta demanda, no sabemos cuánto más se habría vendido. Tres: el modelo se queda corto cuando las ventas crecen, como vimos en 2026. Y cuatro: julio todavía no se puede validar. En resumen, tres resultados: un modelo sencillo que mejora un 31 % a la mejor referencia y que probamos sin trampas; una previsión de 2 398 bicis para julio con una recomendación de stock concreta; y cuatro perfiles de cliente, cada uno con su acción. Muchas gracias. ¿Preguntas?»

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
- [ ] `uv run python src/modelo.py entrenar` y después `uv run python src/presentacion.py` generan la presentación.
- [ ] Cada miembro sabe explicar: la pregunta, la clave de una fila, entrenamiento / validación / prueba, por qué no usar `revenue` y un perfil de cliente.
- [ ] Autoevaluación rellenada.
- [ ] Ensayo cronometrado entre 15 y 20 minutos (objetivo: 17:30), con las demos incluidas.
