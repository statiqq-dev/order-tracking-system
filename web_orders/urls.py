"""Маршруты страниц заказов."""

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders, name='list'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('statistics/', views.statistics, name='statistics'),
]
