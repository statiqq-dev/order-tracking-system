"""Страницы списка товаров и отдельного товара."""

from pathlib import Path

from django.shortcuts import render

from domain.products import find_product
from infrastructure.json_storage import load_products_from_json

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def products(request):
    """Показывает список товаров из JSON-файла."""
    products_list = load_products_from_json(DATA_DIR / 'products.json')

    context = {
        'products': products_list,
    }

    return render(request, 'product_pages/product_list.html', context)


def product_detail(request, product_id):
    """Показывает товар или страницу с кодом 404."""
    products_list = load_products_from_json(DATA_DIR / 'products.json')
    product = find_product(products_list, product_id)

    context = {
        'product': product,
    }

    return render(
        request,
        'product_pages/product_detail.html',
        context,
        status=404 if product is None else 200,
    )
