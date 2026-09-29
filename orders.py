"""Класс заказа и операции с коллекцией заказов."""

from __future__ import annotations

from collections.abc import Iterator

from clients import Client, find_client
from products import Product, find_product
from utils import generate_id


class Order:
    """Заказ клиента на выбранный товар."""

    def __init__(
        self, order_id: int, client: Client, product: Product,
        quantity: int, is_ready: bool = False,
    ) -> None:
        """Создает заказ и связывает клиента с товаром."""
        if quantity <= 0:
            raise ValueError('Количество должно быть больше нуля.')
        self.id = order_id
        self.client = client
        self.product = product
        self.quantity = quantity
        self.is_ready = is_ready

    @classmethod
    def from_data(
        cls, data: dict, client: Client, product: Product,
    ) -> Order:
        """Создает заказ из данных JSON и связанных объектов."""
        return cls(
            data['id'], client, product, data['quantity'], data['is_ready'],
        )

    def calculate_total(self) -> float:
        """Рассчитывает полную стоимость заказа."""
        return calculate_order_price(self.product.price, self.quantity)

    def change_status(self, is_ready: bool) -> None:
        """Изменяет статус готовности заказа."""
        self.is_ready = is_ready

    def get_status(self) -> str:
        """Возвращает текстовый статус заказа."""
        return get_order_status(self.is_ready)

    def __str__(self) -> str:
        """Возвращает строковое представление заказа."""
        return (f'Заказ ID: {self.id}, Клиент: {self.client.name}, '
                f'Товар: {self.product.name}, Количество: {self.quantity}, '
                f'Сумма: {self.calculate_total():.2f}, '
                f'Статус: {self.get_status()}')


def add_order(
    orders: list[Order], client_id: int, product_id: int,
    quantity: int, clients: list[Client], products: list[Product],
) -> Order:
    """Создает заказ для существующего клиента после проверки данных."""
    client = find_client(clients, client_id)
    if client is None:
        raise ValueError('Клиент с таким ID не найден.')
    product = find_product(products, product_id)
    if product is None:
        raise ValueError('Товар с таким ID не найден.')
    order = Order(generate_id(orders), client, product, quantity)
    orders.append(order)
    return order


def find_order_by_id(orders: list[Order], order_id: int) -> Order | None:
    """Возвращает заказ по ID или None."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def delete_order(orders: list[Order], order_id: int) -> None:
    """Удаляет (отменяет) заказ по ID."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        raise ValueError('Заказ с таким ID не найден.')
    orders.remove(order)


def change_order_status(
    orders: list[Order], order_id: int, is_ready: bool,
) -> None:
    """Устанавливает булев статус готовности заказа."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        raise ValueError('Заказ с таким ID не найден.')
    order.change_status(is_ready)


def find_orders_by_client(
    orders: list[Order], client_id: int,
) -> list[Order]:
    """Находит все заказы клиента."""
    return [order for order in orders if order.client.id == client_id]


def find_orders(orders: list[Order], query: str) -> list[Order]:
    """Ищет заказы по подстроке названия товара без учета регистра."""
    query = query.strip().lower()
    return [order for order in orders if query in order.product.name.lower()]


def filter_orders_by_status(
    orders: list[Order], is_ready: bool,
) -> Iterator[Order]:
    """Генерирует заказы с выбранным статусом."""
    for order in orders:
        if order.is_ready == is_ready:
            yield order


def calculate_order_price(price: float, quantity: int) -> float:
    """Рассчитывает стоимость заказа (сценарий ПР1)."""
    return round(price * quantity, 2)


def get_order_status(is_ready: bool) -> str:
    """Возвращает текстовый статус (сценарий ПР1)."""
    if is_ready:
        return 'Заказ готов к выдаче'
    return 'Заказ находится в обработке'


def sort_orders(
    orders: list[Order], key: str = 'total', reverse: bool = False,
) -> list[Order]:
    """Сортирует копию списка по сумме, товару или ID."""
    if key == 'total':
        return sorted(orders, reverse=reverse,
                      key=lambda order: order.calculate_total())
    if key == 'product_name':
        return sorted(orders, reverse=reverse,
                      key=lambda order: order.product.name.lower())
    if key == 'id':
        return sorted(orders, reverse=reverse, key=lambda order: order.id)
    raise ValueError('Допустимые ключи: total, product_name, id.')


def get_order_statistics(orders: list[Order]) -> dict:
    """Возвращает количество, статусы, сумму и число клиентов с заказами."""
    ready = 0
    amount: float = 0.0
    client_ids = set()
    for order in orders:
        if order.is_ready:
            ready += 1
        amount += order.calculate_total()
        client_ids.add(order.client.id)
    return {
        'total': len(orders),
        'ready': ready,
        'processing': len(orders) - ready,
        'clients': len(client_ids),
        'amount': round(amount, 2),
    }
