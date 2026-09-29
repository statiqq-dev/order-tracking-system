"""Класс клиента и операции с коллекцией клиентов."""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import generate_id

if TYPE_CHECKING:
    from orders import Order


class Client:
    """Клиент системы учета заказов."""

    def __init__(self, client_id: int, name: str, phone: str) -> None:
        """Создает клиента после проверки данных."""
        name = name.strip()
        phone = phone.strip()
        if not name or not phone:
            raise ValueError('Заполните имя и телефон.')
        self.id = client_id
        self.name = name
        self.phone = phone

    @classmethod
    def from_data(cls, data: dict) -> Client:
        """Создает клиента из данных JSON."""
        return cls(data['id'], data['name'], data['phone'])

    def __str__(self) -> str:
        """Возвращает строковое представление клиента."""
        return f'Клиент ID: {self.id}, Имя: {self.name}, Телефон: {self.phone}'


def find_client(clients: list[Client], client_id: int) -> Client | None:
    """Находит клиента по ID."""
    for client in clients:
        if client.id == client_id:
            return client
    return None


def find_clients(clients: list[Client], query: str) -> list[Client]:
    """Ищет по подстроке имени без учета регистра."""
    query = query.strip().lower()
    return [client for client in clients if query in client.name.lower()]


def delete_client(
    clients: list[Client], client_id: int, orders: list[Order],
) -> None:
    """Удаляет клиента, только если у него нет заказов."""
    client = find_client(clients, client_id)
    if client is None:
        raise ValueError('Клиент с таким ID не найден.')
    for order in orders:
        if order.client is client:
            raise ValueError('Сначала удалите заказы этого клиента.')
    clients.remove(client)


def add_client(clients: list[Client], name: str, phone: str) -> Client:
    """Создает и добавляет нового клиента."""
    client = Client(generate_id(clients), name, phone)
    clients.append(client)
    return client
