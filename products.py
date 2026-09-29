"""Операции с товарами без файлового ввода-вывода."""

from utils import generate_id


def find_product(products: list[dict], product_id: int) -> dict | None:
    """Находит товар по ID."""
    for product in products:
        if product['id'] == product_id:
            return product
    return None


def find_products(products: list[dict], query: str) -> list[dict]:
    """Ищет товары по подстроке названия без учета регистра."""
    query = query.strip().lower()
    return [product for product in products
            if query in product['name'].lower()]


def add_product(products: list[dict], name: str, price: float) -> dict:
    """Проверяет данные и добавляет товар."""
    name = name.strip()
    if not name:
        raise ValueError('Введите название товара.')
    if price <= 0:
        raise ValueError('Цена должна быть больше нуля.')
    product = {
        'id': generate_id(products),
        'name': name,
        'price': price,
    }
    products.append(product)
    return product


def update_product(
    products: list[dict], product_id: int, name: str, price: float,
) -> None:
    """Изменяет название и цену существующего товара."""
    product = find_product(products, product_id)
    if product is None:
        raise ValueError('Товар с таким ID не найден.')
    name = name.strip()
    if not name:
        raise ValueError('Введите название товара.')
    if price <= 0:
        raise ValueError('Цена должна быть больше нуля.')
    product['name'] = name
    product['price'] = price


def delete_product(
    products: list[dict], product_id: int, orders: list[dict],
) -> None:
    """Удаляет товар, только если он не используется в заказах."""
    product = find_product(products, product_id)
    if product is None:
        raise ValueError('Товар с таким ID не найден.')
    for order in orders:
        if order['product_id'] == product_id:
            raise ValueError('Сначала удалите заказы с этим товаром.')
    products.remove(product)
