"""Ввод и проверка значений для консольного интерфейса."""


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
