"""Общий HTML-каркас страниц проекта ПР5."""


def page(title: str, content: str) -> str:
    """Вставляет содержимое страницы в общий HTML-каркас."""
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
