"""Страницы списка товаров и отдельного товара."""

from pathlib import Path

from django.http import HttpResponse

from homepage.views import page
from products import find_product
from storage import load_products_from_json

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def products(request):
    """Показывает список товаров из JSON-файла."""
    items = ''
    for product in load_products_from_json(DATA_DIR / 'products.json'):
        items += f'''
        <li class="list-group-item d-flex justify-content-between">
            <a href="/products/{product.id}/">{product.name}</a>
            <span>{product.price:.2f} руб.</span>
        </li>
        '''
    content = f'''
    <h1>Товары</h1>
    <ul class="list-group">{items}</ul>
    '''
    return HttpResponse(page('Система учета заказов - товары', content))


def product_detail(request, product_id):
    """Показывает товар или возвращает код 404."""
    products_list = load_products_from_json(DATA_DIR / 'products.json')
    product = find_product(products_list, product_id)

    if product is None:
        content = '''
        <h1 class="text-danger">Товар не найден</h1>
        <a href="/products/" class="btn btn-outline-secondary">
            К списку товаров
        </a>
        '''
        return HttpResponse(
            page('Товар не найден', content),
            status=404,
        )

    content = f'''
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{product.name}</h5>
            <p class="card-text"><strong>ID:</strong> {product.id}</p>
            <p class="card-text">
                <strong>Цена:</strong> {product.price:.2f} руб.
            </p>
            <a href="/products/" class="btn btn-outline-secondary">
                К списку товаров
            </a>
        </div>
    </div>
    '''
    return HttpResponse(page(product.name, content), status=200)
