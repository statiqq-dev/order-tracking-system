"""Подключение к базе данных SQLite."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'data' / 'order_tracking.sqlite'


def get_connection():
    """Открывает соединение с проверкой внешних ключей и доступом по именам."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def fetch_all(query, params=()):
    """Выполняет SELECT и возвращает все строки результата."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def fetch_one(query, params=()):
    """Выполняет SELECT и возвращает одну строку или None."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()
