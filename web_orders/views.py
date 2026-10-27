"""Страницы заказов: список, отдельный заказ и статистика."""

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from product_pages.models import Product

from .models import Client, Order

# Сколько заказов нужно, чтобы клиент считался постоянным.
REGULAR_CLIENT_ORDERS = 3
ORDERS_PER_PAGE = 3

# Сумма заказа: количество, умноженное на цену связанного товара.
ORDER_TOTAL = F('quantity') * F('product__price')

# Допустимые значения параметра sort и соответствующие поля модели.
SORT_FIELDS = {
    'id': 'id',
    'client': 'client__name',
    'product': 'product__name',
    'total': '-total',
}


def orders(request):
    """Показывает заказы с поиском, фильтрами, сортировкой и страницами."""
    query = request.GET.get('q', '').strip()
    client_id = request.GET.get('client', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', 'id')

    orders_list = Order.objects.annotate(total=ORDER_TOTAL)

    if query:
        orders_list = orders_list.filter(
            Q(client__name__icontains=query)
            | Q(product__name__icontains=query)
        )
    if client_id.isdigit():
        orders_list = orders_list.filter(client_id=int(client_id))
    if status == 'ready':
        orders_list = orders_list.filter(is_ready=True)
    elif status == 'processing':
        orders_list = orders_list.exclude(is_ready=True)

    orders_list = orders_list.order_by(
        SORT_FIELDS.get(sort, 'id'), 'id',
    ).values(
        'id', 'is_ready', 'total',
        client_name=F('client__name'),
        product_name=F('product__name'),
    )

    page_obj = Paginator(orders_list, ORDERS_PER_PAGE).get_page(
        request.GET.get('page'),
    )

    context = {
        'orders': page_obj,
        'page_obj': page_obj,
        'clients': Client.objects.all(),
        'query': query,
        'selected_client': client_id,
        'status': status,
        'sort': sort,
    }

    return render(request, 'web_orders/order_list.html', context)


def order_detail(request, order_id):
    """Показывает заказ с клиентом и товаром или страницу с кодом 404."""
    order = get_object_or_404(
        Order.objects.select_related('client', 'product')
        .annotate(total=ORDER_TOTAL),
        pk=order_id,
    )

    context = {
        'order': order,
    }

    return render(request, 'web_orders/order_detail.html', context)


def statistics(request):
    """Показывает сводку, статистику по клиентам и товарам."""
    summary = Order.objects.aggregate(
        orders_count=Count('id'),
        ready_count=Count('id', filter=Q(is_ready=True)),
        total_amount=Sum(ORDER_TOTAL, default=0),
    )
    prices = Product.objects.aggregate(
        min_price=Min('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
    )
    # Запрос строится от Client, поэтому клиенты без заказов тоже попадают
    # в результат (аналог LEFT JOIN) со значением 0.
    clients = Client.objects.annotate(
        orders_count=Count('orders'),
        total_amount=Sum(
            F('orders__quantity') * F('orders__product__price'), default=0,
        ),
    ).order_by('-total_amount')
    products = Product.objects.annotate(
        quantity_sum=Sum('orders__quantity', default=0),
    ).order_by('-quantity_sum')
    regular_clients = clients.filter(
        orders_count__gte=REGULAR_CLIENT_ORDERS,
    ).order_by('-orders_count')

    context = {
        'summary': summary,
        'prices': prices,
        'clients': clients,
        'products': products,
        'regular_clients': regular_clients,
        'regular_client_orders': REGULAR_CLIENT_ORDERS,
    }

    return render(request, 'web_orders/statistics.html', context)
