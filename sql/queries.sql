-- =========================================
-- Система учета заказов: SQL-запросы
-- Значения после ? в приложении передаются параметрами.
-- =========================================

-- ---------- Выборка списков ----------

-- 1. Список товаров по названию (страница /products/)
SELECT id, name, price
FROM products
ORDER BY name;

-- 2. Список клиентов по имени
SELECT id, name, phone
FROM clients
ORDER BY name;

-- ---------- Фильтрация WHERE ----------

-- 3. Товар по идентификатору (страница /products/<id>/)
SELECT id, name, price
FROM products
WHERE id = 1;

-- 4. Товары не дороже заданной цены (поиск /products/search/)
SELECT id, name, price
FROM products
WHERE price <= 5000
ORDER BY price;

-- 5. Заказы, которые ещё в обработке
SELECT id, client_id, product_id, quantity
FROM orders
WHERE is_ready = 0
ORDER BY id;

-- ---------- Соединение таблиц JOIN ----------

-- 6. Заказы с клиентом, товаром и суммой (страница /orders/)
SELECT
    orders.id,
    orders.quantity,
    orders.is_ready,
    clients.name AS client_name,
    products.name AS product_name,
    orders.quantity * products.price AS total
FROM orders
JOIN clients ON orders.client_id = clients.id
JOIN products ON orders.product_id = products.id
ORDER BY orders.id;

-- 7. Полная информация о заказе (страница /orders/<id>/)
SELECT
    orders.id,
    orders.quantity,
    orders.is_ready,
    clients.name AS client_name,
    clients.phone AS client_phone,
    products.id AS product_id,
    products.name AS product_name,
    orders.quantity * products.price AS total
FROM orders
JOIN clients ON orders.client_id = clients.id
JOIN products ON orders.product_id = products.id
WHERE orders.id = 1;

-- ---------- Агрегатные функции ----------

-- 8. Сводка по заказам: количество, готовые, общая сумма (статистика)
SELECT
    COUNT(*) AS orders_count,
    SUM(orders.is_ready) AS ready_count,
    SUM(orders.quantity * products.price) AS total_amount
FROM orders
JOIN products ON orders.product_id = products.id;

-- 9. Минимальная, средняя и максимальная цена товара (статистика)
SELECT
    MIN(price) AS min_price,
    AVG(price) AS avg_price,
    MAX(price) AS max_price
FROM products;

-- ---------- Группировка GROUP BY ----------

-- 10. Количество заказов и сумма по каждому клиенту (статистика)
--     LEFT JOIN оставляет клиентов без заказов со значением 0.
SELECT
    clients.name AS client_name,
    COUNT(orders.id) AS orders_count,
    COALESCE(SUM(orders.quantity * products.price), 0) AS total_amount
FROM clients
LEFT JOIN orders ON orders.client_id = clients.id
LEFT JOIN products ON orders.product_id = products.id
GROUP BY clients.id, clients.name
ORDER BY total_amount DESC;

-- 11. Сколько единиц каждого товара заказано (статистика)
SELECT
    products.name AS product_name,
    COALESCE(SUM(orders.quantity), 0) AS quantity_sum
FROM products
LEFT JOIN orders ON orders.product_id = products.id
GROUP BY products.id, products.name
ORDER BY quantity_sum DESC;

-- ---------- Фильтрация групп HAVING ----------

-- 12. Постоянные клиенты: три заказа и больше (статистика)
SELECT
    clients.name AS client_name,
    COUNT(orders.id) AS orders_count
FROM clients
JOIN orders ON orders.client_id = clients.id
GROUP BY clients.id, clients.name
HAVING COUNT(orders.id) >= 3
ORDER BY orders_count DESC;
