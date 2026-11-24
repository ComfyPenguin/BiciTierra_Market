# BiciTierra Market

**Memoria del proyecto**

Predicción mensual de ventas y segmentación de clientes

**Equipo:** Andy, Guillem y Dennis

Caso práctico de aprendizaje automático con datos sintéticos.

## Índice

- [1. Introducción y marco del proyecto](#1-introducción-y-marco-del-proyecto)
  - [1.1. Introducción](#11-introducción)
  - [1.2. Objetivos](#12-objetivos)
- [2. Diseño del proyecto](#2-diseño-del-proyecto)
  - [2.1. Enfoque para la previsión de ventas](#21-enfoque-para-la-previsión-de-ventas)
  - [2.2. Enfoque para la segmentación de clientes](#22-enfoque-para-la-segmentación-de-clientes)
  - [2.3. Selección de los modelos](#23-selección-de-los-modelos)
- [3. Diseño del proyecto](#3-diseño-del-proyecto)
  - [3.1. Análisis de los requisitos del sistema](#31-análisis-de-los-requisitos-del-sistema)
  - [3.2. Casos de uso del sistema](#32-casos-de-uso-del-sistema)
  - [3.3. Tecnologías](#33-tecnologías)
  - [3.4. Arquitectura](#34-arquitectura)
  - [3.5. Seguridad, privacidad y control de accesos](#35-seguridad-privacidad-y-control-de-accesos)
- [4. Flujo de trabajo](#4-flujo-de-trabajo)
  - [4.1. Planificación y gestión de tareas](#41-planificación-y-gestión-de-tareas)
  - [4.2. Reparto de tareas](#42-reparto-de-tareas)
- [5. Procesamiento de datos](#5-procesamiento-de-datos)
  - [5.1. Obtención y origen de los datos](#51-obtención-y-origen-de-los-datos)
  - [5.2. Manipulación y transformación de datos](#52-manipulación-y-transformación-de-datos)
  - [5.3. Almacenamiento](#53-almacenamiento)
  - [5.4. Ingesta de datos y visualización](#54-ingesta-de-datos-y-visualización)
- [6. Inteligencia artificial y aprendizaje automático](#6-inteligencia-artificial-y-aprendizaje-automático)
  - [6.1. Modelo de previsión mensual de ventas](#61-modelo-de-previsión-mensual-de-ventas)
    - [6.1.1. Estrategia de entrenamiento, hiperparámetros y resultados](#611-estrategia-de-entrenamiento-hiperparámetros-y-resultados)
    - [6.1.2. Estudio comparativo y elección del modelo](#612-estudio-comparativo-y-elección-del-modelo)
  - [6.2. Segmentación de clientes con K-Means](#62-segmentación-de-clientes-con-k-means)
  - [6.3. Aplicación del modelo a la previsión de julio](#63-aplicación-del-modelo-a-la-previsión-de-julio)
- [7. Desarrollo del sistema](#7-desarrollo-del-sistema)
  - [7.1. Backend](#71-backend)
  - [7.2. Frontend](#72-frontend)
- [8. Conclusiones y líneas futuras](#8-conclusiones-y-líneas-futuras)
  - [8.1. Problemas surgidos durante el desarrollo](#81-problemas-surgidos-durante-el-desarrollo)
  - [8.2. Funcionalidades pendientes y líneas futuras](#82-funcionalidades-pendientes-y-líneas-futuras)
  - [8.3. Conclusiones generales](#83-conclusiones-generales)
- [9. Bibliografía y fuentes](#9-bibliografía-y-fuentes)
  - [9.1. Conjuntos de datos utilizados](#91-conjuntos-de-datos-utilizados)
  - [9.2. APIs externas](#92-apis-externas)
  - [9.3. Documentación y evidencias](#93-documentación-y-evidencias)

## 1. Introducción y marco del proyecto

### 1.1. Introducción

BiciTierra Market vende bicicletas urbanas, de montaña y eléctricas en tiendas físicas y por Internet. Opera en tres regiones: costa, interior y área metropolitana. Las combinaciones de canal, línea y región forman 18 series comerciales. La dirección necesita anticipar las ventas para distribuir el stock y conocer mejor a sus clientes para orientar las campañas.

### 1.2. Objetivos

- Estimar las unidades vendidas del mes siguiente para cada serie comercial con la información disponible antes de que empiece el mes.
- Agrupar a los clientes por su comportamiento de compra y proponer una acción para cada perfil.
- Reunir las ventas observadas, la evaluación del modelo, la previsión de julio y los perfiles de cliente en un panel que permita consultar los resultados.

## 2. Diseño del proyecto

### 2.1. Enfoque para la previsión de ventas

La media histórica de cada serie ofrece una primera referencia. Repetir las ventas del mismo mes del año anterior incorpora la estacionalidad y proporciona una segunda referencia. A partir de ambas se valora cuánto aporta un modelo que también tenga en cuenta el stock, las campañas y la tendencia.

### 2.2. Enfoque para la segmentación de clientes

Se parte de una clasificación por reglas comerciales y se compara con K-Means, que agrupa a los clientes según la distancia entre sus perfiles. La comparación permite comprobar si los grupos obtenidos distinguen comportamientos útiles para decidir una acción comercial.

### 2.3. Selección de los modelos

En ventas, se eligió Ridge con `alpha = 100` por su rendimiento en la validación temporal. En clientes, se eligió K-Means con cuatro grupos porque permitía distinguir perfiles con acciones diferentes. El capítulo 6 recoge la comparación y los resultados de ambas decisiones.

## 3. Diseño del proyecto

### 3.1. Análisis de los requisitos del sistema

La previsión debe devolver una cantidad por serie y mes. Los predictores se limitan a los datos disponibles al tomar la decisión de stock y las ventas previstas quedan entre cero y las existencias iniciales. La segmentación utiliza una ficha por cliente. Cada perfil debe interpretarse a partir de variables de comportamiento y vincularse con una acción comercial.

### 3.2. Casos de uso del sistema

- **Responsable de stock.** Consulta la previsión y las existencias por canal, línea y región.
- **Equipo comercial.** Consulta los perfiles para elegir una acción para cada segmento.
- **Equipo de análisis.** Revisa las métricas y las predicciones por serie.

### 3.3. Tecnologías

Python y Jupyter sirven para explorar los datos y documentar los experimentos. pandas y NumPy preparan las tablas y las variables. scikit-learn implementa la regresión Ridge y K-Means. joblib guarda el modelo entrenado. El panel y la presentación se distribuyen como archivos HTML. El entorno se gestiona con uv.

### 3.4. Arquitectura

Los CSV de `data/originales/` alimentan tres notebooks dedicados a exploración, previsión y segmentación. Estos generan métricas, predicciones y perfiles. Los scripts de `src/` reproducen el modelo de ventas y generan el panel y la presentación a partir de los datos y resultados guardados.

### 3.5. Seguridad, privacidad y control de accesos

El caso práctico usa datos sintéticos. `customer_id` identifica los registros al guardar la asignación de segmentos y queda fuera del entrenamiento de K-Means. El panel muestra perfiles agregados. Los HTML generados se abren como archivos estáticos y carecen de cuentas de usuario.

## 4. Flujo de trabajo

### 4.1. Planificación y gestión de tareas

| Semana | Trabajo registrado |
|---|---|
| 1 | Explorar los datos, formular el problema y preparar la primera referencia (CP1). |
| 2 | Preparar las particiones, los retardos y la referencia estacional (CP2). |
| 3 | Comparar Ridge con las referencias y analizar errores de validación. |
| 4 | Segmentar a los clientes y fijar el modelo de ventas antes de la prueba (CP3). |
| 5 | Evaluar enero-junio de 2026 y preparar la previsión de julio. |
| 6 | Reunir el panel, la memoria y la presentación para la defensa (CP4). |

### 4.2. Reparto de tareas

| Miembro | Trabajo |
|---|---|
| Andy | Referencia por medias de grupo, métricas por campaña y región, y cuaderno de seguimiento. |
| Dennis | Análisis exploratorio, ficha del CP1, preparación y modelado de ventas, presentación y memoria. |
| Guillem | Segmentación de clientes y panel de resultados. |

## 5. Procesamiento de datos

### 5.1. Obtención y origen de los datos

| Fichero | Contenido | Unidad de observación |
|---|---|---|
| `sales_history.csv` | 1 188 registros, de enero de 2021 a junio de 2026 | Mes, canal, línea y región |
| `sales_forecast_input.csv` | 18 registros de julio de 2026 con entradas para la previsión | Mes, canal, línea y región |
| `customers.csv` | 2 000 clientes a 30 de junio de 2026 | Cliente |

El análisis de ventas hasta 2024 planteó dos hipótesis. La primera fue que las ventas son estacionales. En bicicletas de montaña, la media pasó de 63 unidades por serie en enero a 131 en julio. La segunda fue que las bicicletas eléctricas y el canal en línea mostraban una tendencia al alza. Las ventas de eléctricas aumentaron un 28 % entre 2021 y 2024.

### 5.2. Manipulación y transformación de datos

| Incidencia | Tratamiento |
|---|---|
| Nulos en presupuesto y descuento previstos | Imputación con la mediana del periodo de entrenamiento |
| Nulos en gasto real, descuento real y sesiones web | Esas variables se conocen al cierre y quedan fuera de la previsión |
| Agotamiento de existencias en 228 registros (19,2 %) | Se conserva la venta observada y se limita la previsión al stock inicial |
| Gasto anual ausente en 30 clientes | Se reconstruye multiplicando el valor medio del pedido por los pedidos del último año |
| Recencia ausente en 20 clientes | Se imputa con la mediana de días desde el último pedido |
| Edad ausente en 20 clientes | La edad queda fuera de la segmentación |

Los retardos `lag_1` y `lag_12` recuperan las ventas de la misma serie uno y doce meses antes. El modelo utiliza también el calendario, la tendencia y las variables comerciales conocidas de antemano. Los ingresos del propio mes, el stock final y la rotura de stock quedan excluidos por fuga de información. En el notebook, reconstruir las ventas con los ingresos del mismo mes produce un error prácticamente nulo.

### 5.3. Almacenamiento

Los CSV originales se conservan en `data/originales/`. La asignación de segmentos por cliente se guarda en `data/derivados/`. Las métricas, las predicciones, los perfiles, el modelo y los HTML se guardan en `evidencies/`.

### 5.4. Ingesta de datos y visualización

El panel se genera por lotes a partir de los CSV. Agrupa las unidades vendidas por mes y línea de producto y cruza la previsión de julio con las existencias iniciales de cada serie. La previsión aparece diferenciada de las ventas observadas.

## 6. Inteligencia artificial y aprendizaje automático

### 6.1. Modelo de previsión mensual de ventas

#### 6.1.1. Estrategia de entrenamiento, hiperparámetros y resultados

La evaluación reproduce una previsión a un mes. Cada predicción puede usar las ventas de los meses ya cerrados. Los datos se dividen por fechas para que el modelo aprenda del pasado y su rendimiento se mida en meses posteriores.

| Periodo | Registros | Uso |
|---|---|---|
| 2021 | 216 | Historial para calcular `lag_12` |
| 2022-2024 | 648 | Entrenamiento |
| 2025 | 216 | Validación y selección |
| Enero-junio de 2026 | 108 | Prueba final |

Las categorías se codifican en columnas binarias y las variables se estandarizan. El mes se representa mediante seno y coseno, también por línea de producto, para recoger el ciclo anual. Ridge penaliza los coeficientes grandes y `alpha` controla la intensidad de la penalización.

El **MAE** indica cuántas bicicletas se desvía la predicción, en promedio, por serie y mes. El **WAPE** divide la suma de los errores absolutos entre la suma de las ventas observadas y la expresa en porcentaje.

#### 6.1.2. Estudio comparativo y elección del modelo

| Modelo | MAE en validación | WAPE en validación |
|---|---|---|
| Media de la serie | 18,75 | 18,06 % |
| Mismo mes del año anterior | 17,40 | 16,77 % |
| Ridge, `alpha = 1` | 12,43 | 11,98 % |
| Ridge, `alpha = 10` | 12,37 | 11,92 % |
| **Ridge, alpha = 100** | **12,05** | **11,61 %** |

Ridge con `alpha = 100` redujo el MAE un 31 % frente a la referencia estacional en 2025. La validación cruzada temporal sobre 2023, 2024 y 2025 también respaldó este ajuste, con un MAE medio de 11,32. Se evaluaron pesos para meses recientes, una tendencia por canal y más retardos. La mejor variante bajó a 11,18, una diferencia de alrededor del 1 %, y se mantuvo el modelo más sencillo.

En la prueba, Ridge obtuvo **16,14 unidades de MAE** y **13,53 % de WAPE**. La referencia estacional obtuvo 21,24 y 17,81 %, respectivamente. La previsión quedó 14,3 unidades por debajo de la venta observada en promedio. Por ejemplo, en abril de 2026 se pronosticaron 230 bicicletas urbanas en línea para la región metropolitana y se vendieron 328. En los 21 registros de prueba con rotura de stock, la previsión quedó por debajo de la venta observada.

Un ensayo posterior que incluyó 2025 en el entrenamiento redujo el MAE de prueba a 14,08 y el WAPE a 11,80 %. El ensayo se hizo después de consultar la prueba. El resultado principal corresponde al modelo fijado antes de abrirla.

### 6.2. Segmentación de clientes con K-Means

Se utilizaron el gasto anual y el número de pedidos en escala logarítmica, los días desde el último pedido, la proporción de devoluciones y la antigüedad. Se estandarizaron las cinco variables para que sus unidades de medida no dominaran las distancias. El valor medio del pedido se dejó fuera por su relación directa con el gasto y el número de pedidos.

Se compararon de dos a siete grupos. Con dos, la silueta fue de 0,285 y la separación principal fue entre clientes activos e inactivos. Con cuatro, la silueta fue de aproximadamente 0,24 y se obtuvieron perfiles con acciones diferenciadas. El gasto y los pedidos de la tabla son medianas. La proporción de devoluciones es una media.

| Segmento | Clientes | Perfil | Acción propuesta |
|---|---|---|---|
| Fieles veteranos | 650 | 1 350 €, 6 pedidos y unos 8 años de antigüedad | Programa de fidelidad |
| Nuevos activos | 644 | 1 456 €, 6 pedidos y unos 2,5 años de antigüedad | Bienvenida al segundo año |
| Ocasionales inactivos | 532 | 216 €, 2 pedidos y casi cuatro meses sin comprar | Reactivación con el servicio técnico |
| Devoluciones altas | 174 | 369 €, 3 pedidos y un 40 % de devoluciones | Revisar las causas de las devoluciones |

K-Means distinguió clientes de alto gasto que las reglas agrupaban entre los ocasionales e identificó un perfil con muchas devoluciones. Para 270 clientes (13,5 %) los dos centros más próximos quedan a distancias parecidas, por lo que su asignación es menos clara.

### 6.3. Aplicación del modelo a la previsión de julio

La entrada de julio de 2026 contiene 18 series y 2 951 bicicletas en stock. Ridge estimó **2 398 ventas**. Las ventas reales de julio quedan fuera del histórico disponible, de modo que esta cifra sigue pendiente de validación.

La previsión llega al stock disponible en tres series de tienda física: urbanas en interior, montaña en el área metropolitana y eléctricas en interior. La recomendación fue reforzar el stock de esas series y valorar un margen de unas 14 unidades en el canal en línea de la región metropolitana y en urbanas, donde el modelo tendió a quedarse corto.

## 7. Desarrollo del sistema

### 7.1. Backend

El procesamiento se ejecuta con notebooks y scripts locales. `src/modelo.py` encapsula la imputación, la codificación, el escalado y la regresión Ridge en un pipeline de scikit-learn. Al entrenar, reproduce el error del notebook y guarda el modelo en `evidencies/modelo_ridge.joblib`. El comando de predicción carga ese modelo y aplica los límites de stock a julio.

Desde la raíz del repositorio, estos comandos preparan el entorno y abren Jupyter:

```bash
uv sync
uv run jupyter lab
```

Los notebooks se ejecutan desde `notebooks/`, en el orden `01_eda.ipynb`, `02_modelatge_baseline.ipynb` y `03_segmentacio.ipynb`. Con sus resultados guardados, se puede entrenar el modelo y generar el panel y la presentación desde la raíz:

```bash
uv run python src/modelo.py entrenar
uv run python src/panel.py
uv run python src/presentacion.py
```

### 7.2. Frontend

El panel `evidencies/panel.html` muestra las ventas por mes y línea, las métricas de los modelos, la previsión de julio por serie y los perfiles de cliente. La tabla de julio señala las series en las que la previsión alcanza las existencias.

La presentación `evidencies/presentacion.html` reúne las visualizaciones de la defensa. Incluye una demostración del pipeline de ventas y un simulador para explorar el efecto del stock sobre la previsión de julio.

## 8. Conclusiones y líneas futuras

### 8.1. Problemas surgidos durante el desarrollo

La disponibilidad de las variables obligó a separar los planes del mes de lo que se conoce al cierre. La rotura de stock impide medir las ventas que habrían sido posibles con más existencias. En 2026, la venta media por serie y mes aumentó de 104 a 119 unidades respecto a 2025, y el modelo quedó por debajo de las ventas observadas. En la segmentación, los casos próximos a dos centros limitan la confianza en algunas asignaciones.

### 8.2. Funcionalidades pendientes y líneas futuras

La previsión de julio queda pendiente de contrastar con las ventas reales. La campaña de verano coincide con la temporada alta. La propuesta fue mantenerla y medir su efecto con una prueba por regiones. Para valorar las acciones de fidelización, reactivación y servicio hacen falta compras posteriores a la fecha de la ficha de clientes.

### 8.3. Conclusiones generales

Ridge mejoró la referencia estacional en validación y en la prueba final. La previsión de julio permitió localizar tres series en las que las existencias podrían limitar las ventas. K-Means proporcionó cuatro perfiles para proponer acciones comerciales diferenciadas. Los resultados ilustran el método con datos sintéticos y requieren validación con datos reales antes de aplicarlos al negocio.

## 9. Bibliografía y fuentes

### 9.1. Conjuntos de datos utilizados

- Histórico de ventas, entrada de julio y fichas de clientes. [`sales_history.csv`](../data/originales/sales_history.csv), [`sales_forecast_input.csv`](../data/originales/sales_forecast_input.csv) y [`customers.csv`](../data/originales/customers.csv).
- Descripción de las variables. [`DICCIONARI_DADES.md`](../data/originales/DICCIONARI_DADES.md).

### 9.2. APIs externas

El procesamiento de datos y el entrenamiento se ejecutan localmente. El panel carga la biblioteca Chart.js desde una CDN para dibujar los gráficos en el navegador.

### 9.3. Documentación y evidencias

- Exploración, previsión y segmentación. [`01_eda.ipynb`](../notebooks/01_eda.ipynb), [`02_modelatge_baseline.ipynb`](../notebooks/02_modelatge_baseline.ipynb) y [`03_segmentacio.ipynb`](../notebooks/03_segmentacio.ipynb).
- Seguimiento semanal y defensa. [`tareas_semanales.ipynb`](tareas_semanales.ipynb) y [`defensa.md`](defensa.md).
- Evaluación y previsión. [`metricas_modelos.csv`](../evidencies/metricas_modelos.csv), [`prediccions_prova_2026.csv`](../evidencies/prediccions_prova_2026.csv) y [`prediccions_juliol_2026.csv`](../evidencies/prediccions_juliol_2026.csv).
- Perfiles y asignaciones. [`perfil_segmentos.csv`](../evidencies/perfil_segmentos.csv) y [`segmentos_clientes.csv`](../data/derivados/segmentos_clientes.csv).
