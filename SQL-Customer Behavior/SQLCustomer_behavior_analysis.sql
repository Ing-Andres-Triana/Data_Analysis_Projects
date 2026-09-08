# 1. Cual es el gasto promedio por categoria?

SELECT 
Category,
AVG(Purchase_amount) AS average_purchase_amount
FROM customer_behavior
WHERE purchase_amount IS NOT NULL
GROUP BY Category
ORDER BY average_purchase_amount DESC;


# 2. Metodo de pago con mayor monto

SELECT 
Payment_Method,
SUM(Purchase_amount) AS total_compra
FROM customer_behavior
GROUP BY Payment_Method
ORDER BY total_compra DESC;

# 3.¿Cómo varía el rating promedio de reseñas según el tipo de envío?

SELECT 
Shipping_type,
AVG(Rating) AS AVG_RATING
FROM customer_behavior
GROUP BY Shipping_type
ORDER BY AVG_RATING DESC;

# 4.¿Qué porcentaje de clientes tiene suscripción activa, segmentado por género?

SELECT
Gender,
COUNT(*) AS total_clientes,
SUM(CASE WHEN `Subscription_Status` = 'Yes' THEN 1 ELSE 0 END) AS clientes_con_suscripcion,
ROUND(
	SUM(CASE WHEN `Subscription_Status` = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS porcentaje_suscritos
FROM customer_behavior
GROUP BY Gender;

# 5. ¿Los clientes con descuento aplicado compran, en promedio, más o menos que los que no lo tienen?

SELECT 
Discount,
COUNT(*) AS total_clientes,
ROUND(AVG(Purchase_amount),2) AS gasto_promedio
FROM customer_behavior
GROUP BY Discount;

#6. ¿Cuáles son las 5 ubicaciones (Location) con mayor número de compras registradas?
SELECT 
Location,
SUM(Purchase_amount) AS Total_compras
FROM Customer_behavior
GROUP BY Location
ORDER BY Total_compras DESC
LIMIT 5;

#7.¿Cómo se distribuyen los clientes por rango de edad (joven, adulto, mayor) y cuál es su gasto promedio?

SELECT 
CASE WHEN Age < 25 THEN 'Joven'
WHEN Age BETWEEN 25 AND 50 THEN 'Adulto'
ELSE 'Mayor' 
END AS Rango_edad,
AVG(Purchase_amount) AS Compra_promedio
FROM Customer_behavior
GROUP BY 
CASE WHEN Age < 25 THEN 'Joven'
WHEN Age BETWEEN 25 AND 50 THEN 'Adulto'
ELSE 'Mayor' END 
ORDER BY Compra_promedio DESC;
