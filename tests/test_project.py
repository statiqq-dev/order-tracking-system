"""Проверки объектной модели системы учета заказов."""

import json

import pytest

from domain.clients import Client, add_client, delete_client, find_clients
from domain.orders import (
    Order, add_order, calculate_order_price, change_order_status,
    filter_orders_by_status, find_orders, get_order_statistics, sort_orders,
)
from domain.products import (
    Product, add_product, delete_product, update_product,
)
from infrastructure.json_storage import (
    load_clients_from_json, load_orders_from_json, load_products_from_json,
    save_clients_to_json, save_orders_to_json, save_products_to_json,
)


def test_client_creation_and_string():
    client = Client(1, 'Иван', '1234567')
    assert client.id == 1
    assert client.name == 'Иван'
    assert str(client) == 'Клиент ID: 1, Имя: Иван, Телефон: 1234567'


def test_client_collection_operations():
    clients = []
    client = add_client(clients, 'Иван', '1234567')
    assert clients == [client]
    assert find_clients(clients, 'ИВ') == [client]


def test_product_creation_update_and_string():
    product = Product(1, 'Клавиатура', 3500)
    product.update('Механическая клавиатура', 4000)
    assert product.name == 'Механическая клавиатура'
    assert product.price == 4000
    assert str(product).endswith('Цена: 4000.00')


def test_product_collection_operations():
    products = []
    product = add_product(products, 'Клавиатура', 3500)
    update_product(products, product.id, 'Мышь', 1500)
    assert products == [product]
    assert product.name == 'Мышь'


def test_order_connects_client_and_product():
    client = Client(1, 'Иван', '1234567')
    product = Product(1, 'Клавиатура', 3500)
    order = Order(1, client, product, 2)
    assert order.client is client
    assert order.product is product
    assert order.calculate_total() == 7000
    assert 'Клиент: Иван' in str(order)


def test_calculate_order_price():
    assert calculate_order_price(3500, 2) == 7000


def test_add_order_and_change_status():
    client = Client(1, 'Иван', '1234567')
    product = Product(1, 'Клавиатура', 3500)
    orders = []
    order = add_order(orders, 1, 1, 2, [client], [product])
    change_order_status(orders, order.id, True)
    assert orders == [order]
    assert order.is_ready
    assert order.get_status() == 'Заказ готов к выдаче'


def test_unknown_client_or_product():
    client = Client(1, 'Иван', '1234567')
    product = Product(1, 'Клавиатура', 3500)
    with pytest.raises(ValueError):
        add_order([], 99, 1, 2, [client], [product])
    with pytest.raises(ValueError):
        add_order([], 1, 99, 2, [client], [product])


def test_linked_objects_cannot_be_deleted():
    client = Client(1, 'Иван', '1234567')
    product = Product(1, 'Клавиатура', 3500)
    order = Order(1, client, product, 2)
    with pytest.raises(ValueError):
        delete_client([client], client.id, [order])
    with pytest.raises(ValueError):
        delete_product([product], product.id, [order])


def test_search_filter_sort_and_statistics():
    client = Client(1, 'Иван', '1234567')
    keyboard = Product(1, 'Клавиатура', 3500)
    mouse = Product(2, 'Мышь', 1500)
    orders = [
        Order(1, client, keyboard, 2, True),
        Order(2, client, mouse, 1),
    ]
    assert find_orders(orders, 'КЛАВ') == [orders[0]]
    assert list(filter_orders_by_status(orders, True)) == [orders[0]]
    assert sort_orders(orders, 'total') == [orders[1], orders[0]]
    assert get_order_statistics(orders) == {
        'total': 2,
        'ready': 1,
        'processing': 1,
        'clients': 1,
        'amount': 8500,
    }


def test_json_round_trip_restores_objects(tmp_path):
    clients_path = tmp_path / 'clients.json'
    products_path = tmp_path / 'products.json'
    orders_path = tmp_path / 'orders.json'
    client = Client(1, 'Иван', '1234567')
    product = Product(1, 'Клавиатура', 3500)
    order = Order(1, client, product, 2)

    save_clients_to_json(clients_path, [client])
    save_products_to_json(products_path, [product])
    save_orders_to_json(orders_path, [order])

    clients = load_clients_from_json(clients_path)
    products = load_products_from_json(products_path)
    orders = load_orders_from_json(orders_path, clients, products)
    assert isinstance(clients[0], Client)
    assert isinstance(products[0], Product)
    assert isinstance(orders[0], Order)
    assert orders[0].client is clients[0]
    assert orders[0].product is products[0]


def test_order_with_unknown_link_is_rejected(tmp_path):
    orders_path = tmp_path / 'orders.json'
    orders_path.write_text(json.dumps([{
        'id': 1,
        'client_id': 99,
        'product_id': 1,
        'quantity': 2,
        'is_ready': False,
    }]), encoding='utf-8')
    product = Product(1, 'Клавиатура', 3500)
    with pytest.raises(ValueError):
        load_orders_from_json(orders_path, [], [product])
