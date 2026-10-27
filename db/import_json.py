"""Перенос данных из JSON-файлов в базу SQLite.

Запуск из корня проекта: python -m db.import_json
"""

import json

from db.database import BASE_DIR, get_connection

DATA_DIR = BASE_DIR / 'data'
SCHEMA_FILE = BASE_DIR / 'sql' / 'schema.sql'


def load_json(filename):
    """Читает список записей из JSON-файла каталога data."""
    with open(DATA_DIR / filename, encoding='utf-8') as file:
        return json.load(file)


def create_schema(conn):
    """Создает таблицы по файлу sql/schema.sql."""
    conn.executescript(SCHEMA_FILE.read_text(encoding='utf-8'))


def import_clients(conn):
    """Добавляет клиентов из JSON одной командой executemany()."""
    conn.executemany(
        'INSERT INTO clients (id, name, phone) VALUES (?, ?, ?)',
        [
            (client['id'], client['name'], client['phone'])
            for client in load_json('clients.json')
        ],
    )


def import_products(conn):
    """Добавляет товары из JSON одной командой executemany()."""
    conn.executemany(
        'INSERT INTO products (id, name, price) VALUES (?, ?, ?)',
        [
            (product['id'], product['name'], product['price'])
            for product in load_json('products.json')
        ],
    )


def import_orders(conn):
    """Добавляет заказы из JSON одной командой executemany()."""
    conn.executemany(
        '''
        INSERT INTO orders (id, client_id, product_id, quantity, is_ready)
        VALUES (?, ?, ?, ?, ?)
        ''',
        [
            (
                order['id'],
                order['client_id'],
                order['product_id'],
                order['quantity'],
                int(order['is_ready']),
            )
            for order in load_json('orders.json')
        ],
    )


def import_data(conn):
    """Заменяет содержимое таблиц данными из JSON.

    Заказы ссылаются на клиентов и товары, поэтому удаляются первыми,
    а добавляются последними.
    """
    conn.execute('DELETE FROM orders')
    conn.execute('DELETE FROM products')
    conn.execute('DELETE FROM clients')
    import_clients(conn)
    import_products(conn)
    import_orders(conn)


def main():
    conn = get_connection()
    try:
        create_schema(conn)
        import_data(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
