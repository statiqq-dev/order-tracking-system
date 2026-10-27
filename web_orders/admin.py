"""Настройки административной панели заказов."""

from django.contrib import admin

from .models import Client, Order

admin.site.register(Client)
admin.site.register(Order)
