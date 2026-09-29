"""Проверка данных и безопасный ввод из консоли."""

from collections.abc import Sequence
from typing import Protocol


class HasId(Protocol):
    """Объект с целочисленным идентификатором."""

    id: int


def generate_id(records: Sequence[HasId]) -> int:
    """Возвращает ID, не занятый в текущей коллекции."""
    if not records:
        return 1
    return max(record.id for record in records) + 1


def input_int(message: str) -> int:
    """Повторяет ввод до получения целого числа."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print('Введите целое число.')


def input_float(message: str) -> float:
    """Повторяет ввод до получения числа."""
    while True:
        try:
            return float(input(message).replace(',', '.'))
        except ValueError:
            print('Введите число.')
