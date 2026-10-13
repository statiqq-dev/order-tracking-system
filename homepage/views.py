"""Главная страница и обработчик ошибки 404."""

from django.http import HttpResponse

from order_tracking.html import page


def index(request):
    """Показывает главную страницу проекта."""
    content = '''
    <h1 class="display-4">Система учета заказов</h1>
    <p class="lead">Веб-интерфейс для просмотра товаров и заказов.</p>
    <p>Основные разделы:</p>
    <a href="/products/" class="btn btn-primary me-2">Товары</a>
    <a href="/orders/" class="btn btn-secondary">Заказы</a>
    '''
    return HttpResponse(page('Система учета заказов', content))


def page_not_found(request, exception):
    """Возвращает общую страницу для несуществующего адреса."""
    content = '''
    <h1 class="text-danger">404 - страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    '''
    return HttpResponse(
        page('404 - страница не найдена', content),
        status=404,
    )
