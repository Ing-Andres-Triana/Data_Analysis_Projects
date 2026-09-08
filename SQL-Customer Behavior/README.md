# 🛍️ Análisis de Comportamiento de Compra de Clientes con SQL

Análisis exploratorio de datos de clientes de retail usando **SQL puro** (agregaciones, `GROUP BY`, `CASE WHEN`) para responder preguntas de negocio reales sobre gasto, retención, envíos y segmentación de clientes.

## 📊 Sobre el dataset

Dataset de comportamiento de compra con **1,000 registros** de clientes, incluyendo:

`Customer ID` · `Age` · `Gender` · `Item_Purchased` · `Category` · `Purchase_amount` · `Location` · `Size` · `Color` · `Season` · `Rating` · `Subscription_Status` · `Shipping_type` · `Discount` · `Previous_purchases` · `Payment_Method` · `Frequency_purchases`

## 🎯 Objetivo

Practicar y demostrar consultas SQL aplicadas a un caso de negocio real: entender qué categorías, ubicaciones, métodos de pago y segmentos de clientes son más rentables o relevantes para la toma de decisiones.

## 🔍 Preguntas de negocio y hallazgos clave

### 1. ¿Cuál es el gasto promedio por categoría?
```sql
SELECT Category, AVG(Purchase_amount) AS average_purchase_amount
FROM customer_behavior
WHERE Purchase_amount IS NOT NULL
GROUP BY Category
ORDER BY average_purchase_amount DESC;
```
📈 **Footwear** lidera con el ticket promedio más alto (~$60.7), aunque las 4 categorías están bastante parejas entre sí.

### 2. ¿Qué método de pago genera el mayor monto total de ventas?
```sql
SELECT Payment_Method, SUM(Purchase_amount) AS total_compra
FROM customer_behavior
GROUP BY Payment_Method
ORDER BY total_compra DESC;
```
💳 **Tarjeta de crédito** es el método que más ingresos totales genera.

### 3. ¿Cómo varía el rating promedio según el tipo de envío?
```sql
SELECT Shipping_type, AVG(Rating) AS avg_rating
FROM customer_behavior
GROUP BY Shipping_type
ORDER BY avg_rating DESC;
```
⭐ El envío **Standard** tiene el rating promedio más alto, aunque las diferencias entre tipos de envío son mínimas.

### 4. ¿Qué porcentaje de clientes tiene suscripción activa, por género?
```sql
SELECT
    Gender,
    COUNT(*) AS total_clientes,
    SUM(CASE WHEN Subscription_Status = 'Yes' THEN 1 ELSE 0 END) AS clientes_con_suscripcion,
    ROUND(SUM(CASE WHEN Subscription_Status = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS porcentaje_suscritos
FROM customer_behavior
GROUP BY Gender;
```
🚨 **Hallazgo más llamativo del análisis:** el 38.6% de los clientes hombres tiene suscripción activa, mientras que **0% de las clientas mujeres** están suscritas. Esto sugiere una oportunidad clara para revisar la estrategia de suscripciones dirigida al público femenino.

### 5. ¿Los clientes con descuento compran más o menos, en promedio?
```sql
SELECT
    Discount,
    COUNT(*) AS total_clientes,
    ROUND(AVG(Purchase_amount), 2) AS gasto_promedio
FROM customer_behavior
GROUP BY Discount;
```
🏷️ Los clientes **sin** descuento gastan ligeramente más en promedio ($60.11) que los que sí usan descuento ($58.75) — el descuento no está impulsando mayor gasto por transacción.

### 6. ¿Cuáles son las 5 ubicaciones con más compras registradas?
```sql
SELECT Location, COUNT(*) AS total_compras
FROM customer_behavior
GROUP BY Location
ORDER BY total_compras DESC
LIMIT 5;
```
📍 **Montana** y **Arkansas** encabezan el ranking en número de transacciones.

### 7. ¿Cómo se distribuyen los clientes por rango de edad y su gasto promedio?
```sql
SELECT
    CASE
        WHEN Age < 25 THEN 'Joven'
        WHEN Age BETWEEN 25 AND 50 THEN 'Adulto'
        ELSE 'Mayor'
    END AS rango_edad,
    AVG(Purchase_amount) AS compra_promedio
FROM customer_behavior
GROUP BY
    CASE
        WHEN Age < 25 THEN 'Joven'
        WHEN Age BETWEEN 25 AND 50 THEN 'Adulto'
        ELSE 'Mayor'
    END
ORDER BY compra_promedio DESC;
```
👥 El segmento **Adulto (25-50 años)** tiene el gasto promedio más alto, aunque los tres grupos etarios gastan de forma bastante similar.

## 🧠 Conceptos SQL aplicados

- Funciones de agregación: `AVG()`, `SUM()`, `COUNT()`
- Agrupamiento de datos con `GROUP BY`
- Lógica condicional con `CASE WHEN` (creación de categorías personalizadas y conteos condicionales)
- Ordenamiento y filtrado de resultados: `ORDER BY`, `LIMIT`, `WHERE`
- Cálculo de porcentajes y tasas dentro de una consulta SQL

## 🛠️ Herramientas

- **SQL** (compatible con MySQL / SQLite / PostgreSQL)
- Dataset en formato `.csv`

---

📌 *Proyecto realizado como práctica de análisis de datos con SQL, enfocado en traducir preguntas de negocio en consultas concretas y hallazgos accionables.*
