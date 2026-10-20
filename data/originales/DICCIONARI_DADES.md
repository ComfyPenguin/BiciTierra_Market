# Diccionario de datos · BiciTierra Market

Todos los valores son sintéticos. Importes en EUR; proporciones entre 0 y 1 (0.15 significa 15%). Nulo no significa cero. Los periodos son los de la simulación.

## Ventas mensuales

| Campo | Tipo / unidad | Definición y disponibilidad |
|---|---|---|
| month | texto YYYY-MM | Mes que se quiere predecir; conocido antes |
| channel | categoría | `store` o `ecommerce`; conocido antes |
| product_line | categoría | `urban`, `mountain`, `electric`; conocido antes |
| region | categoría | `coast`, `inland`, `metro`; conocido antes |
| marketing_spend | decimal EUR | Gasto real del mes; al cierre; puede faltar |
| avg_discount | proporción | Descuento efectivo del mes; al cierre; puede faltar |
| stock_units | entero unidades | Disponibilidad inicial del mes; conocida antes. No es el stock final |
| website_sessions | entero visitas | Sesiones del mes atribuidas a la celda comercial, también como apoyo a la tienda; al cierre; puede faltar |
| sales_units | entero unidades | Objetivo: unidades vendidas; al cierre, limitadas por el stock |
| revenue | decimal EUR | Ingresos netos de descuento, sin impuestos; al cierre; no es predictor de las unidades del mismo mes |
| marketing_budget | decimal EUR | Presupuesto aprobado antes del mes; puede faltar en el extracto histórico |
| planned_discount | proporción | Descuento previsto antes del mes; puede faltar en el extracto histórico |
| list_price | decimal EUR/unidad | Precio de tarifa representativo fijado antes del mes |
| campaign | categoría | Plan simulado: `none`, `spring`, `summer`, `black_friday`, `christmas`; conocido antes, no es un calendario comercial real |
| days_in_month | entero días | Número de días naturales del mes; conocido antes |
| closing_stock_units | entero unidades | `stock_units - sales_units`; al cierre; no es predictor anticipado |
| stockout | entero 0/1 | 1 si la demanda simulada supera la disponibilidad; solo al cierre |

No hay reposición dentro del mes. Por eso `sales_units <= stock_units` y el stock final nunca es negativo. No se publica la demanda no atendida; el fichero permite explicar la censura por stock, no evaluar una predicción exacta de la demanda latente.

## Entrada de predicción

`sales_forecast_input.csv` usa los diez campos conocidos antes del mes: `month`, `channel`, `product_line`, `region`, `stock_units`, `marketing_budget`, `planned_discount`, `list_price`, `campaign`, `days_in_month`.

Contiene julio de 2026 y no incluye columnas de objetivo vacías: no hay que confundir la ausencia de resultado con ventas cero. Los retardos se obtienen del histórico con la clave completa y el mes correcto.

## Clientes

| Campo | Tipo / unidad | Definición |
|---|---|---|
| customer_id | identificador | Clave ficticia única; hay que excluirla del clustering |
| age | entero años | Edad entre 18 y 79; puede faltar |
| city | categoría | Gandia, Oliva, Sueca, Alzira, Tavernes o Carcaixent; ubicación ficticia |
| channel_preference | categoría | `store` o `ecommerce` |
| annual_spend | decimal EUR | Importe acumulado de pedidos de los últimos 12 meses, antes de devoluciones; puede faltar |
| avg_order_value | decimal EUR/pedido | Ticket medio de los últimos 12 meses |
| orders_last_12m | entero pedidos | Pedidos en los últimos 12 meses; muestra de clientes con al menos una compra |
| returns_ratio | proporción | `returned_orders_last_12m / orders_last_12m`, redondeado a cuatro decimales |
| bike_interest | categoría | `urban`, `mountain`, `electric` o `service` |
| service_interest | categoría | `low`, `medium`, `high` |
| snapshot_date | texto YYYY-MM-DD | Fecha de corte 2026-06-30; común a toda la muestra |
| tenure_months | entero meses | Antigüedad de 2 a 120 meses |
| days_since_last_order | entero días | Recencia en la fecha de corte, entre 0 y 364; puede faltar |
| returned_orders_last_12m | entero pedidos | Número de pedidos con devolución; no supera el de pedidos |

`annual_spend = avg_order_value × orders_last_12m` con redondeo a céntimos. Si falta el gasto, se puede reconstruir en este caso simulado; hay que justificarlo. No hay datos posteriores a la fotografía ni etiqueta de compra futura: este CSV sirve para segmentación, no para validar una predicción de churn o de compras futuras.
