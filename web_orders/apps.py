"""Конфигурация приложения заказов."""

from django.apps import AppConfig


class WebOrdersConfig(AppConfig):
    """Конфигурация приложения web_orders."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_orders'
