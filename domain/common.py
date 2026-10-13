"""Общие инструменты предметной области."""

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
