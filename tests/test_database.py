"""Проверки базы данных SQLite и страниц, работающих с ней."""

import json
import os
import sqlite3

import django
from django.test import Client

from db.database import BASE_DIR
from db.import_json import create_schema, import_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracking.settings')
django.setup()


def count_json(filename):
    with open(BASE_DIR / 'data' / filename, encoding='utf-8') as file:
        return len(json.load(file))


def test_import_copies_all_json_records():
    conn = sqlite3.connect(':memory:')
    create_schema(conn)
    import_data(conn)
    for table in ['clients', 'products', 'orders']:
        count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        assert count == count_json(f'{table}.json')
    conn.close()


def test_product_search_uses_parameter():
    text = Client().get('/products/search/?max_price=3500').content.decode()
    assert 'Клавиатура' in text
    assert 'Телевизор' not in text


def test_product_search_without_results():
    text = Client().get('/products/search/?max_price=1').content.decode()
    assert 'Товаров не дороже 1 руб. нет.' in text


def test_statistics_page():
    response = Client().get('/orders/statistics/')
    assert response.status_code == 200
    text = response.content.decode()
    assert 'Заказы по клиентам' in text
    assert 'Пётр Кузнецов' in text
