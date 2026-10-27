"""Перенос данных из базы ПР7 в таблицы Django ORM.

Запуск из корня проекта после migrate: python -m db.import_sqlite_to_orm
"""

import os

import django
from django.db import transaction

from db.database import fetch_all

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracking.settings')
django.setup()

from product_pages.models import Product  # noqa: E402
from web_orders.models import Client, Order  # noqa: E402

# Заказы ссылаются на клиентов и товары, поэтому переносятся последними.
TABLES = [(Client, 'clients'), (Product, 'products'), (Order, 'orders')]


@transaction.atomic
def import_data():
    """Создает или обновляет записи, сохраняя исходные id и связи."""
    for model, table in TABLES:
        for row in fetch_all(f'SELECT * FROM {table}'):
            data = dict(row)
            model.objects.update_or_create(pk=data.pop('id'), defaults=data)


if __name__ == '__main__':
    import_data()
    for model, table in TABLES:
        print(f'{table}: {model.objects.count()}')
