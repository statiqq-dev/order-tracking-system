"""Маршруты страниц товаров."""

from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products, name='list'),
    path('<int:product_id>/', views.product_detail, name='detail'),
    path('search/', views.product_search, name='search'),
]
