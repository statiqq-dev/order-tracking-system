"""Главная страница и обработчик ошибки 404."""

from django.shortcuts import render


def index(request):
    """Показывает главную страницу проекта."""
    return render(request, 'homepage/index.html')


def page_not_found(request, exception):
    """Возвращает общую страницу для несуществующего адреса."""
    return render(request, 'homepage/404.html', status=404)
