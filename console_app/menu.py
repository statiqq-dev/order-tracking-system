"""Консольный интерфейс системы учета заказов."""

from pathlib import Path

from .input import input_float, input_int
from domain.clients import Client, add_client, delete_client, find_clients
from domain.orders import (
    Order, add_order, change_order_status, delete_order,
    filter_orders_by_status, find_orders, find_orders_by_client,
    get_order_statistics, sort_orders,
)
from domain.products import (
    Product, add_product, delete_product, find_product, find_products,
    update_product,
)
from infrastructure.json_storage import (
    load_clients_from_json, load_orders_from_json, load_products_from_json,
    save_clients_to_json, save_orders_to_json, save_products_to_json,
)

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
MENU = '''
===== Система учета заказов =====
1. Показать все заказы
2. Найти заказы клиента
3. Добавить заказ
4. Изменить статус заказа
5. Удалить (отменить) заказ
6. Показать список клиентов
7. Добавить клиента
8. Удалить клиента
9. Найти заказы по товару
10. Отфильтровать заказы по статусу
11. Сортировать заказы
12. Статистика заказов
13. Найти клиента по имени
14. Показать список товаров
15. Добавить товар
16. Изменить товар
17. Удалить товар
18. Найти товар по названию
0. Выход
'''


def show_orders(orders: list[Order]) -> None:
    """Показывает заказы с именем клиента, суммой и статусом."""
    if not orders:
        print('Заказов нет.')
    for order in orders:
        print(order)


def show_clients(clients: list[Client]) -> None:
    """Показывает клиентов в соответствии со схемой JSON."""
    if not clients:
        print('Клиентов нет.')
    for client in clients:
        print(client)


def show_products(products: list[Product]) -> None:
    """Показывает товары в соответствии со схемой JSON."""
    if not products:
        print('Товаров нет.')
    for product in products:
        print(product)


def input_status() -> bool:
    """Принимает только 0 (в обработке) или 1 (готов)."""
    status = input_int('Статус (0 - в обработке, 1 - готов): ')
    if status not in (0, 1):
        raise ValueError('Статус должен быть 0 или 1.')
    return bool(status)


def execute_action(
    answer: str, orders: list[Order], clients: list[Client],
    products: list[Product],
) -> None:
    """Выполняет один пункт меню над переданными коллекциями."""
    match answer:
        case '1':
            show_orders(orders)
        case '2':
            client_id = input_int('ID клиента: ')
            show_orders(find_orders_by_client(orders, client_id))
        case '3':
            client_id = input_int('ID клиента: ')
            product_id = input_int('ID товара: ')
            quantity = input_int('Количество: ')
            add_order(orders, client_id, product_id, quantity, clients,
                      products)
        case '4':
            order_id = input_int('ID заказа: ')
            change_order_status(orders, order_id, input_status())
        case '5':
            delete_order(orders, input_int('ID заказа: '))
        case '6':
            show_clients(clients)
        case '7':
            add_client(clients, input('Имя: '), input('Телефон: '))
        case '8':
            delete_client(clients, input_int('ID клиента: '), orders)
        case '9':
            show_orders(find_orders(orders, input('Название товара: ')))
        case '10':
            show_orders(list(filter_orders_by_status(orders, input_status())))
        case '11':
            key = input('Поле (total, product_name, id): ').strip()
            direction = input('Порядок (1 - возрастание, 2 - убывание): ')
            if direction not in ('1', '2'):
                raise ValueError('Порядок должен быть 1 или 2.')
            show_orders(sort_orders(orders, key, direction == '2'))
        case '12':
            stats = get_order_statistics(orders)
            print(f"Всего: {stats['total']}; готовы: {stats['ready']}; "
                  f"в обработке: {stats['processing']}; "
                  f"клиентов с заказами: {stats['clients']}; "
                  f"сумма: {stats['amount']:.2f}")
        case '13':
            show_clients(find_clients(clients, input('Имя клиента: ')))
        case '14':
            show_products(products)
        case '15':
            add_product(products, input('Название: '),
                        input_float('Цена: '))
        case '16':
            product_id = input_int('ID товара: ')
            if find_product(products, product_id) is None:
                raise ValueError('Товар с таким ID не найден.')
            update_product(products, product_id, input('Новое название: '),
                           input_float('Новая цена: '))
        case '17':
            delete_product(products, input_int('ID товара: '), orders)
        case '18':
            show_products(find_products(products, input('Название товара: ')))
        case _:
            raise ValueError('Некорректный выбор. Попробуйте снова.')


def main(data_dir: Path = DATA_DIR) -> None:
    """Загружает данные и сохраняет каждую успешную операцию меню."""
    clients_path = data_dir / 'clients.json'
    orders_path = data_dir / 'orders.json'
    products_path = data_dir / 'products.json'
    try:
        clients = load_clients_from_json(clients_path)
        products = load_products_from_json(products_path)
        orders = load_orders_from_json(orders_path, clients, products)
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        print(f'Ошибка загрузки данных: {error}')
        print('Исправьте JSON-файлы и перезапустите программу.')
        return

    try:
        while True:
            print(MENU)
            answer = input('Выберите действие: ').strip()
            try:
                if answer != '0':
                    execute_action(answer, orders, clients, products)
            except (ValueError, KeyError, TypeError) as error:
                print(f'Операция не выполнена: {error}')
                continue

            # Сохраняем после изменения данных и перед обычным выходом.
            if answer in ('3', '4', '5', '7', '8', '15', '16', '17', '0'):
                try:
                    save_clients_to_json(clients_path, clients)
                    save_orders_to_json(orders_path, orders)
                    save_products_to_json(products_path, products)
                    print('Данные сохранены.')
                except OSError as error:
                    print(f'Не удалось сохранить данные: {error}')
                    print('Изменения остались в памяти. Для повторной '
                          'попытки сохранения выберите 0.')
                    continue
            if answer == '0':
                break
    except (EOFError, KeyboardInterrupt):
        print('\nВвод завершен.')
    print('Выход из программы.')
