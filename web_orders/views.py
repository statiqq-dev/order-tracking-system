"""Страницы списка заказов и отдельного заказа."""

from pathlib import Path

from django.http import HttpResponse

from domain.orders import find_order_by_id
from infrastructure.json_storage import (
    load_clients_from_json,
    load_orders_from_json,
    load_products_from_json,
)
from order_tracking.html import page

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def load_project_data():
    """Загружает связанные объекты проекта из JSON-файлов."""
    clients = load_clients_from_json(DATA_DIR / 'clients.json')
    products = load_products_from_json(DATA_DIR / 'products.json')
    orders = load_orders_from_json(
        DATA_DIR / 'orders.json',
        clients,
        products,
    )
    return orders


def orders(request):
    """Показывает список заказов из JSON-файла."""
    items = ''
    for order in load_project_data():
        badge = 'bg-success' if order.is_ready else 'bg-warning text-dark'
        items += f'''
        <li class="list-group-item d-flex justify-content-between">
            <a href="/orders/{order.id}/">
                Заказ №{order.id}: {order.product.name}
            </a>
            <span class="badge {badge}">{order.get_status()}</span>
        </li>
        '''
    content = f'''
    <h1>Заказы</h1>
    <ul class="list-group">{items}</ul>
    '''
    return HttpResponse(page('Система учета заказов - заказы', content))


def order_detail(request, order_id):
    """Показывает заказ или возвращает код 404."""
    order = find_order_by_id(load_project_data(), order_id)

    if order is None:
        content = '''
        <h1 class="text-danger">Заказ не найден</h1>
        <a href="/orders/" class="btn btn-outline-secondary">
            К списку заказов
        </a>
        '''
        return HttpResponse(
            page('Заказ не найден', content),
            status=404,
        )

    badge = 'bg-success' if order.is_ready else 'bg-warning text-dark'
    content = f'''
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заказ №{order.id}</h5>
            <p class="card-text">
                <strong>Клиент:</strong> {order.client.name}
            </p>
            <p class="card-text">
                <strong>Товар:</strong> {order.product.name}
            </p>
            <p class="card-text">
                <strong>Количество:</strong> {order.quantity}
            </p>
            <p class="card-text">
                <strong>Сумма:</strong> {order.calculate_total():.2f} руб.
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{order.get_status()}</span>
            </p>
            <a href="/orders/" class="btn btn-outline-secondary">
                К списку заказов
            </a>
        </div>
    </div>
    '''
    return HttpResponse(page(f'Заказ №{order.id}', content), status=200)
