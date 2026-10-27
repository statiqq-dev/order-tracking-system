"""Модели клиента и заказа."""

from django.db import models

from product_pages.models import Product


class Client(models.Model):
    """Клиент, оформляющий заказы."""

    name = models.CharField('Имя', max_length=200)
    phone = models.CharField('Телефон', max_length=20)

    class Meta:
        ordering = ['name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ клиента на товар.

    PROTECT запрещает удалить клиента или товар, пока есть их заказы.
    """

    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name='orders',
        verbose_name='Клиент',
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orders',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField('Количество')
    is_ready = models.BooleanField('Готов к выдаче', default=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}: {self.product} ({self.client})'
