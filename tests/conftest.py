"""Общая подготовка тестов: Django и тестовая база с данными ПР7."""

import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracking.settings')
django.setup()


@pytest.fixture(scope='session', autouse=True)
def test_database():
    """Создает тестовую базу миграциями и переносит в неё данные ПР7."""
    from django.test.utils import (
        setup_databases, setup_test_environment, teardown_databases,
    )

    from db.import_sqlite_to_orm import import_data

    setup_test_environment()
    old_config = setup_databases(verbosity=0, interactive=False)
    import_data()
    yield
    teardown_databases(old_config, verbosity=0)
