"""Главная страница и общий HTML-каркас."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Возвращает общий HTML-каркас страницы."""
    bootstrap = (
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/'
        'dist/css/bootstrap.min.css'
    )
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav border-bottom mb-4">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/products/">Товары</a>
        <a class="nav-link" href="/orders/">Заказы</a>
    </nav>
    <main class="container pb-4">{content}</main>
</body>
</html>'''


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
