"""Загрузка и сохранение данных в JSON-файлах."""

import json
from pathlib import Path


def load_records(filename: str | Path) -> list[dict]:
    """Загружает список словарей; отсутствующий файл означает пустой список."""
    try:
        with open(filename, encoding='utf-8') as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError(f'{filename}: ожидается список словарей.')
    return records


def save_records(filename: str | Path, records: list[dict]) -> None:
    """Сохраняет список словарей в JSON с русскими буквами."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_orders_from_json(filename: str | Path) -> list[dict]:
    """Загружает заказы."""
    return load_records(filename)


def load_clients_from_json(filename: str | Path) -> list[dict]:
    """Загружает клиентов."""
    return load_records(filename)


def load_products_from_json(filename: str | Path) -> list[dict]:
    """Загружает товары."""
    return load_records(filename)


def save_orders_to_json(filename: str | Path, orders: list[dict]) -> None:
    """Сохраняет заказы."""
    save_records(filename, orders)


def save_clients_to_json(filename: str | Path, clients: list[dict]) -> None:
    """Сохраняет клиентов."""
    save_records(filename, clients)


def save_products_to_json(filename: str | Path, products: list[dict]) -> None:
    """Сохраняет товары."""
    save_records(filename, products)
