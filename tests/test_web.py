"""Проверки страниц Django-приложения."""

from django.test import Client, override_settings


def test_main_pages():
    client = Client()

    response = client.get('/')
    assert response.status_code == 200
    assert 'Система учета заказов' in response.content.decode()

    response = client.get('/products/')
    assert response.status_code == 200
    assert 'Клавиатура' in response.content.decode()

    response = client.get('/orders/')
    assert response.status_code == 200
    assert 'Заказ №1' in response.content.decode()


def test_detail_pages():
    client = Client()

    response = client.get('/products/1/')
    assert response.status_code == 200
    assert '3500.00 руб.' in response.content.decode()

    response = client.get('/orders/1/')
    assert response.status_code == 200
    text = response.content.decode()
    assert 'Иван Иванов' in text
    assert '7000.00 руб.' in text


def test_unknown_objects_return_404():
    client = Client()
    assert client.get('/products/999/').status_code == 404
    assert client.get('/orders/999/').status_code == 404


@override_settings(DEBUG=False)
def test_custom_404_page():
    response = Client().get('/nonexistent/')
    assert response.status_code == 404
    assert 'страница не найдена' in response.content.decode()


def test_pages_use_base_template_and_static_files():
    text = Client().get('/products/').content.decode()
    assert 'Всего товаров:' in text
    assert '/static/homepage/css/style.css' in text
    assert '/static/homepage/js/main.js' in text
    assert '/static/homepage/img/logo.png' in text
    assert 'href="/products/1/"' in text


def test_order_status_is_rendered_by_include():
    text = Client().get('/orders/1/').content.decode()
    assert 'order-status-processing' in text
    assert 'Заказ находится в обработке' in text
