"""Предметная область системы учета заказов."""

from .clients import Client
from .orders import Order
from .products import Product

__all__ = ['Client', 'Order', 'Product']
