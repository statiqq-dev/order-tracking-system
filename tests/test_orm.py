"""Проверки моделей Django, переноса данных и ORM-запросов."""

import pytest
from django.db.models import ProtectedError
from django.test import Client

from db.database import fetch_one
from product_pages.models import Product
from web_orders.models import Client as OrderClient, Order


def get_text(url):
    return Client().get(url).content.decode()


def test_data_transferred_with_links():
    for model, table in [(OrderClient, 'clients'), (Product, 'products'),
                         (Order, 'orders')]:
        count = fetch_one(f'SELECT COUNT(*) FROM {table}')[0]
        assert model.objects.count() == count
    order = Order.objects.select_related('client', 'product').get(pk=1)
    assert order.client.name == 'Иван Иванов'
    assert order.product.name == 'Клавиатура'
    assert order in order.client.orders.all()


def test_crud_and_protect():
    product = Product.objects.create(name='Тестовый товар', price=100)
    product.price = 150
    product.save()
    assert Product.objects.get(pk=product.pk).price == 150
    product.delete()
    assert not Product.objects.filter(pk=product.pk).exists()
    with pytest.raises(ProtectedError):
        Product.objects.get(pk=1).delete()


def test_product_search_by_name_and_price():
    text = get_text('/products/search/?q=Мо&max_price=20000')
    assert 'Монитор' in text
    assert 'Мышь' not in text
    assert 'Укажите корректную цену.' in get_text(
        '/products/search/?max_price=abc',
    )


def test_product_detail_shows_orders():
    assert 'Заказ №4' in get_text('/products/1/')


def test_orders_filter_search_and_sort():
    text = get_text('/orders/?status=ready')
    assert 'Найдено заказов: 2' in text
    text = get_text('/orders/?status=processing&client=2')
    assert 'Заказ №4' in text
    assert 'Найдено заказов: 1' in text
    assert 'Найдено заказов: 2' in get_text('/orders/?q=Мышь')
    text = get_text('/orders/?sort=total')
    assert text.index('Заказ №2') < text.index('Заказ №1')
    assert 'Найдено заказов: 5' in get_text('/orders/?sort=unknown')


def test_orders_pagination_keeps_parameters():
    text = get_text('/orders/?sort=client')
    assert 'href="?sort=client&amp;page=2"' in text
    assert 'Заказ №5' in get_text('/orders/?page=2')
    assert 'Заказ №1' in get_text('/orders/?page=abc')


def test_statistics_values():
    text = get_text('/orders/statistics/')
    assert '35300.00 руб.' in text
    assert 'Пётр Кузнецов' in text
