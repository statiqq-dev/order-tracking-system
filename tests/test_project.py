"""Простые проверки основных функций проекта."""

import pytest

from clients import add_client
from orders import add_order, calculate_order_price, find_orders
from products import add_product, delete_product, update_product
from storage import load_records, save_records


def test_add_client():
    clients = []
    add_client(clients, 'Иван', '1234567')
    assert clients == [{'id': 1, 'name': 'Иван', 'phone': '1234567'}]


def test_find_orders():
    products = [
        {'id': 1, 'name': 'Клавиатура', 'price': 3500},
        {'id': 2, 'name': 'Мышь', 'price': 1500},
    ]
    orders = [{'product_id': 1}, {'product_id': 2}]
    assert find_orders(orders, products, 'КЛАВ') == [orders[0]]


def test_calculate_order_price():
    assert calculate_order_price(3500, 2) == 7000


def test_unknown_client():
    orders = []
    with pytest.raises(ValueError):
        add_order(orders, 99, 1, 2, [], [])
    assert orders == []


def test_add_order():
    clients = [{'id': 1, 'name': 'Иван', 'phone': '1234567'}]
    products = [{'id': 1, 'name': 'Клавиатура', 'price': 3500}]
    orders = []
    add_order(orders, 1, 1, 2, clients, products)
    assert orders == [{
        'id': 1, 'client_id': 1, 'product_id': 1,
        'quantity': 2, 'is_ready': False,
    }]


def test_product_operations():
    products = []
    product = add_product(products, 'Клавиатура', 3500)
    update_product(products, product['id'], 'Механическая клавиатура', 4000)
    assert product['name'] == 'Механическая клавиатура'
    assert product['price'] == 4000


def test_cannot_delete_ordered_product():
    products = [{'id': 1, 'name': 'Клавиатура', 'price': 3500}]
    orders = [{'product_id': 1}]
    with pytest.raises(ValueError):
        delete_product(products, 1, orders)
    assert len(products) == 1


def test_save_and_load(tmp_path):
    filename = tmp_path / 'clients.json'
    clients = [{'id': 1, 'name': 'Иван', 'phone': '1234567'}]
    save_records(filename, clients)
    assert load_records(filename) == clients
