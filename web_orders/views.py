"""Страницы списка заказов и отдельного заказа."""

from pathlib import Path

from django.shortcuts import render

from domain.orders import find_order_by_id
from infrastructure.json_storage import (
    load_clients_from_json,
    load_orders_from_json,
    load_products_from_json,
)

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
    context = {
        'orders': load_project_data(),
    }

    return render(request, 'web_orders/order_list.html', context)


def order_detail(request, order_id):
    """Показывает заказ или страницу с кодом 404."""
    order = find_order_by_id(load_project_data(), order_id)

    context = {
        'order': order,
    }

    return render(
        request,
        'web_orders/order_detail.html',
        context,
        status=404 if order is None else 200,
    )
