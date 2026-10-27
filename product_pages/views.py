"""Страницы товаров: список, отдельный товар и поиск по цене."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one


def products(request):
    """Показывает список товаров из базы данных."""
    products_list = fetch_all('''
        SELECT id, name, price
        FROM products
        ORDER BY name
    ''')

    context = {
        'products': products_list,
    }

    return render(request, 'product_pages/product_list.html', context)


def product_detail(request, product_id):
    """Показывает товар или страницу с кодом 404."""
    product = fetch_one('''
        SELECT id, name, price
        FROM products
        WHERE id = ?
    ''', [product_id])

    context = {
        'product': product,
    }

    return render(
        request,
        'product_pages/product_detail.html',
        context,
        status=404 if product is None else 200,
    )


def product_search(request):
    """Ищет товары не дороже цены, указанной в форме."""
    max_price = request.GET.get('max_price', '')
    products_list = []

    if max_price:
        products_list = fetch_all('''
            SELECT id, name, price
            FROM products
            WHERE price <= ?
            ORDER BY price
        ''', [max_price])

    context = {
        'products': products_list,
        'max_price': max_price,
    }

    return render(request, 'product_pages/product_search.html', context)
