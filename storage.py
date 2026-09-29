"""Загрузка и сохранение данных в JSON-файлах."""

import json
from pathlib import Path

from clients import Client, find_client
from orders import Order
from products import Product, find_product


def load_records(filename: str | Path) -> list[dict]:
    """Загружает список словарей; отсутствующий файл означает пустой список."""
    try:
        with open(filename, encoding='utf-8') as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError(f'{filename}: ожидается список словарей.')
    return records


def save_records(filename: str | Path, records: list[dict]) -> None:
    """Сохраняет список словарей в JSON с русскими буквами."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_orders_from_json(
    filename: str | Path, clients: list[Client], products: list[Product],
) -> list[Order]:
    """Загружает заказы и восстанавливает связи объектов."""
    orders = []
    for data in load_records(filename):
        client = find_client(clients, data['client_id'])
        product = find_product(products, data['product_id'])
        if client is None or product is None:
            raise ValueError(
                f'{filename}: заказ {data["id"]} ссылается '
                'на неизвестного клиента или товар.'
            )
        orders.append(Order.from_data(data, client, product))
    return orders


def load_clients_from_json(filename: str | Path) -> list[Client]:
    """Загружает клиентов."""
    return [Client.from_data(data) for data in load_records(filename)]


def load_products_from_json(filename: str | Path) -> list[Product]:
    """Загружает товары."""
    return [Product.from_data(data) for data in load_records(filename)]


def save_orders_to_json(filename: str | Path, orders: list[Order]) -> None:
    """Сохраняет заказы."""
    records = [{
        'id': order.id,
        'client_id': order.client.id,
        'product_id': order.product.id,
        'quantity': order.quantity,
        'is_ready': order.is_ready,
    } for order in orders]
    save_records(filename, records)


def save_clients_to_json(filename: str | Path, clients: list[Client]) -> None:
    """Сохраняет клиентов."""
    records = [{
        'id': client.id,
        'name': client.name,
        'phone': client.phone,
    } for client in clients]
    save_records(filename, records)


def save_products_to_json(
    filename: str | Path, products: list[Product],
) -> None:
    """Сохраняет товары."""
    records = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
    } for product in products]
    save_records(filename, records)
