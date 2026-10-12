"""Маршруты верхнего уровня."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('products/', include('product_pages.urls')),
    path('orders/', include('web_orders.urls')),
]

handler404 = 'homepage.views.page_not_found'
