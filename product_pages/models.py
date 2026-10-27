"""Модель товара."""

from django.db import models


class Product(models.Model):
    """Товар, который можно добавить в заказ."""

    name = models.CharField('Название', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
