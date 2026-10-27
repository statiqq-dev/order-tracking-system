"""Страницы заказов: список, отдельный заказ и статистика."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one

# Сколько заказов нужно, чтобы клиент считался постоянным.
REGULAR_CLIENT_ORDERS = 3


def orders(request):
    """Показывает заказы вместе с клиентом, товаром и суммой."""
    orders_list = fetch_all('''
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
        ORDER BY orders.id
    ''')

    context = {
        'orders': orders_list,
    }

    return render(request, 'web_orders/order_list.html', context)


def order_detail(request, order_id):
    """Показывает заказ или страницу с кодом 404."""
    order = fetch_one('''
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
        WHERE orders.id = ?
    ''', [order_id])

    context = {
        'order': order,
    }

    return render(
        request,
        'web_orders/order_detail.html',
        context,
        status=404 if order is None else 200,
    )


def statistics(request):
    """Показывает сводку, статистику по клиентам и товарам."""
    summary = fetch_one('''
        SELECT
            COUNT(*) AS orders_count,
            SUM(orders.is_ready) AS ready_count,
            SUM(orders.quantity * products.price) AS total_amount
        FROM orders
        JOIN products ON orders.product_id = products.id
    ''')
    prices = fetch_one('''
        SELECT
            MIN(price) AS min_price,
            AVG(price) AS avg_price,
            MAX(price) AS max_price
        FROM products
    ''')
    clients = fetch_all('''
        SELECT
            clients.name AS client_name,
            COUNT(orders.id) AS orders_count,
            COALESCE(SUM(orders.quantity * products.price), 0) AS total_amount
        FROM clients
        LEFT JOIN orders ON orders.client_id = clients.id
        LEFT JOIN products ON orders.product_id = products.id
        GROUP BY clients.id, clients.name
        ORDER BY total_amount DESC
    ''')
    products = fetch_all('''
        SELECT
            products.name AS product_name,
            COALESCE(SUM(orders.quantity), 0) AS quantity_sum
        FROM products
        LEFT JOIN orders ON orders.product_id = products.id
        GROUP BY products.id, products.name
        ORDER BY quantity_sum DESC
    ''')
    regular_clients = fetch_all('''
        SELECT
            clients.name AS client_name,
            COUNT(orders.id) AS orders_count
        FROM clients
        JOIN orders ON orders.client_id = clients.id
        GROUP BY clients.id, clients.name
        HAVING COUNT(orders.id) >= ?
        ORDER BY orders_count DESC
    ''', [REGULAR_CLIENT_ORDERS])

    context = {
        'summary': summary,
        'prices': prices,
        'clients': clients,
        'products': products,
        'regular_clients': regular_clients,
        'regular_client_orders': REGULAR_CLIENT_ORDERS,
    }

    return render(request, 'web_orders/statistics.html', context)
