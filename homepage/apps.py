"""Конфигурация приложения главной страницы."""

from django.apps import AppConfig


class HomepageConfig(AppConfig):
    """Конфигурация приложения homepage."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'
