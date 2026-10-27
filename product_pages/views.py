"""Страницы товаров: список, отдельный товар и поиск."""

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render

from .models import Product


def products(request):
    """Показывает список товаров, упорядоченный по названию."""
    context = {
        'products': Product.objects.all(),
    }

    return render(request, 'product_pages/product_list.html', context)


def product_detail(request, product_id):
    """Показывает товар и его заказы или страницу с кодом 404."""
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'orders': product.orders.select_related('client'),
    }

    return render(request, 'product_pages/product_detail.html', context)


def product_search(request):
    """Ищет товары по части названия и максимальной цене."""
    query = request.GET.get('q', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    products_list = Product.objects.order_by('price')
    error = None

    if query:
        products_list = products_list.filter(name__icontains=query)
    if max_price:
        try:
            products_list = products_list.filter(price__lte=max_price)
        except ValidationError:
            error = 'Укажите корректную цену.'

    context = {
        'products': products_list,
        'query': query,
        'max_price': max_price,
        'searched': query or max_price,
        'error': error,
    }

    return render(request, 'product_pages/product_search.html', context)
