"""Класс товара и операции с коллекцией товаров."""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import generate_id

if TYPE_CHECKING:
    from orders import Order


class Product:
    """Товар, доступный для добавления в заказ."""

    def __init__(self, product_id: int, name: str, price: float) -> None:
        """Создает товар после проверки данных."""
        name = name.strip()
        if not name:
            raise ValueError('Введите название товара.')
        if price <= 0:
            raise ValueError('Цена должна быть больше нуля.')
        self.id = product_id
        self.name = name
        self.price = price

    @classmethod
    def from_data(cls, data: dict) -> Product:
        """Создает товар из данных JSON."""
        return cls(data['id'], data['name'], data['price'])

    def update(self, name: str, price: float) -> None:
        """Изменяет название и цену товара."""
        name = name.strip()
        if not name:
            raise ValueError('Введите название товара.')
        if price <= 0:
            raise ValueError('Цена должна быть больше нуля.')
        self.name = name
        self.price = price

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return (f'Товар ID: {self.id}, Название: {self.name}, '
                f'Цена: {self.price:.2f}')


def find_product(products: list[Product], product_id: int) -> Product | None:
    """Находит товар по ID."""
    for product in products:
        if product.id == product_id:
            return product
    return None


def find_products(products: list[Product], query: str) -> list[Product]:
    """Ищет товары по подстроке названия без учета регистра."""
    query = query.strip().lower()
    return [product for product in products
            if query in product.name.lower()]


def add_product(
    products: list[Product], name: str, price: float,
) -> Product:
    """Создает и добавляет товар."""
    product = Product(generate_id(products), name, price)
    products.append(product)
    return product


def update_product(
    products: list[Product], product_id: int, name: str, price: float,
) -> None:
    """Изменяет название и цену существующего товара."""
    product = find_product(products, product_id)
    if product is None:
        raise ValueError('Товар с таким ID не найден.')
    product.update(name, price)


def delete_product(
    products: list[Product], product_id: int, orders: list[Order],
) -> None:
    """Удаляет товар, только если он не используется в заказах."""
    product = find_product(products, product_id)
    if product is None:
        raise ValueError('Товар с таким ID не найден.')
    for order in orders:
        if order.product is product:
            raise ValueError('Сначала удалите заказы с этим товаром.')
    products.remove(product)
