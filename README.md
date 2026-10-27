# Система учета заказов

## Назначение

Приложение предназначено для учета клиентов, товаров и заказов. Консольная
версия ПР3 дополнена базовым веб-интерфейсом на Django 5.2 в рамках ПР5. В ПР6
веб-интерфейс переведён с формирования HTML в Python на шаблоны Django. В ПР7
данные перенесены в базу SQLite, а веб-страницы получают их SQL-запросами.

Приложение позволяет:

- просматривать товары и сведения о конкретном товаре в браузере;
- просматривать заказы и сведения о конкретном заказе в браузере;
- видеть клиента, товар, количество, сумму и статус заказа;
- работать с клиентами, товарами и заказами в консольной версии;
- искать товары по цене и смотреть статистику заказов на сайте;
- искать, фильтровать и сортировать данные;
- хранить данные в JSON-файлах и базе SQLite.

## Используемые технологии

- Python 3;
- Django 5.2;
- Django Template Language (DTL);
- HTML5;
- CSS3 и Bootstrap 5.3;
- JavaScript;
- SQLite, SQL и модуль `sqlite3`;
- pytest;
- flake8.

## Предметная область

Основные сущности проекта:

- `Client` - клиент;
- `Product` - товар;
- `Order` - заказ.

Заказ связывает существующего клиента с товаром. Он хранит количество товара и
статус готовности. Полная стоимость рассчитывается по цене товара и количеству.

## Архитектура

Код разделён по ответственности:

- `domain/` — предметные сущности и операции над ними;
- `infrastructure/` — техническая работа с JSON;
- `db/` — подключение к SQLite и перенос данных из JSON;
- `sql/` — схема базы данных и SQL-запросы;
- `console_app/` — консольное меню и ввод;
- `order_tracking/` — конфигурация Django-сайта;
- `templates/` — общие шаблоны сайта: `base.html` и навигация;
- `homepage/`, `product_pages/`, `web_orders/` — отдельные части веб-интерфейса
  со своими представлениями, маршрутами и шаблонами;
- `data/` — данные;
- `tests/` — автоматические проверки.

Консольная версия работает с объектами `domain` и JSON через `infrastructure`.
Веб-интерфейс получает данные из SQLite через модуль `db`.

## Объектная модель

### Client

Клиент хранит `id`, `name` и `phone`. Метод `from_data()` создает объект из
данных JSON, а `__str__()` формирует строковое представление.

### Product

Товар хранит `id`, `name` и `price`. Метод `update()` изменяет название и цену,
`from_data()` создает объект из JSON, а `__str__()` формирует строковое
представление.

### Order

Заказ хранит `id`, объекты `Client` и `Product`, количество `quantity` и признак
готовности `is_ready`. Основные методы:

- `calculate_total()` - рассчитывает полную стоимость;
- `change_status()` - изменяет статус готовности;
- `get_status()` - возвращает текстовый статус;
- `from_data()` - восстанавливает заказ и его связи из JSON;
- `__str__()` - формирует строковое представление.

## Страницы веб-интерфейса

- `/` - главная страница, описание проекта и навигация;
- `/products/` - список товаров;
- `/products/<int:product_id>/` - страница отдельного товара;
- `/products/search/?max_price=...` - поиск товаров не дороже заданной цены;
- `/orders/` - список заказов с клиентом, товаром и суммой;
- `/orders/<int:order_id>/` - страница отдельного заказа;
- `/orders/statistics/` - статистика заказов по клиентам и товарам;
- `/admin/` - стандартная административная зона Django.

Неизвестный адрес обрабатывается `homepage.views.page_not_found()` через
`handler404`.

Если товар, заказ или адрес не найден, приложение возвращает страницу с кодом
HTTP 404.

## View-функции

- `homepage.views.index()` показывает главную страницу;
- `homepage.views.page_not_found()` показывает общую страницу ошибки 404;
- `product_pages.views.products()` передаёт в шаблон список товаров;
- `product_pages.views.product_detail()` передаёт в шаблон найденный товар;
- `product_pages.views.product_search()` ищет товары по цене из формы;
- `web_orders.views.orders()` передаёт в шаблон список заказов;
- `web_orders.views.order_detail()` передаёт в шаблон найденный заказ;
- `web_orders.views.statistics()` передаёт в шаблон результаты агрегатных
  запросов.

Представления выполняют SQL-запросы, подготавливают контекст и вызывают
`render()`. HTML-строки в Python не формируются, функция `page()` из ПР5 удалена.
Если объект не найден, в шаблон передаётся `None`, а ответ получает код 404:

```python
context = {
    'product': product,
}
return render(
    request,
    'product_pages/product_detail.html',
    context,
    status=404 if product is None else 200,
)
```

## Шаблоны Django

Каталог `templates/` уровня проекта подключён в `settings.py` через
`'DIRS': [BASE_DIR / 'templates']`. Шаблоны приложений лежат в их каталогах
`templates/<приложение>/` и находятся благодаря `APP_DIRS`.

- `templates/base.html` — общий каркас: кодировка, Bootstrap, собственные CSS и
  JavaScript, логотип, навигация, подвал и блоки `{% block title %}` и
  `{% block content %}`;
- `templates/includes/navigation.html` — навигация, подключается через
  `{% include %}`;
- все страницы наследуют каркас через `{% extends "base.html" %}`;
- `product_pages/includes/product_card.html` — карточка товара в списке;
- `web_orders/includes/order_status.html` — статус заказа, используется в
  списке и на странице заказа.

В шаблонах используются циклы `{% for %}` с `{% empty %}` для пустых коллекций и
условия `{% if %}` для статуса заказа и случая, когда объект не найден.

## Фильтры шаблонов

- `{{ products|length }}` и `{{ orders|length }}` — количество записей;
- `{{ product.name|default:"Без названия" }}` — значение по умолчанию;
- `{{ product.price|floatformat:"2u" }}` — цена с двумя знаками после точки.

Фильтры отвечают только за представление данных, бизнес-логика остаётся в
`domain/`.

## URL-маршрутизация

Приложения имеют пространства имён (`app_name`), маршруты — имена:

- `homepage:index`;
- `products:list`, `products:detail`;
- `orders:list`, `orders:detail`.

Ссылки в шаблонах строятся через `{% url %}`, например
`{% url 'products:detail' product.id %}`, а не через жёстко заданные адреса.

## Статические файлы

Статические файлы находятся в `homepage/static/homepage/` и подключаются в
`base.html` после `{% load static %}`:

- `css/style.css` — собственное оформление шапки, карточек товаров, статусов
  заказов и подвала;
- `js/main.js` — выводит текущий год в подвале;
- `img/logo.png` — логотип в шапке сайта.

Bootstrap используется для базовой вёрстки, собственный CSS — для оформления
проекта.

## База данных

Файл базы: `data/order_tracking.sqlite`. Структура описана в `sql/schema.sql`.

### Таблицы

`clients` — клиенты:

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | первичный ключ |
| `name` | TEXT | имя клиента |
| `phone` | TEXT | телефон |

`products` — товары:

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | первичный ключ |
| `name` | TEXT | название товара |
| `price` | REAL | цена |

`orders` — заказы:

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | первичный ключ |
| `client_id` | INTEGER | внешний ключ на `clients.id` |
| `product_id` | INTEGER | внешний ключ на `products.id` |
| `quantity` | INTEGER | количество |
| `is_ready` | INTEGER | 0 — в обработке, 1 — готов |

Все поля объявлены `NOT NULL`, у `is_ready` значение по умолчанию 0. Один клиент
и один товар могут встречаться во многих заказах, каждый заказ ссылается ровно
на одного клиента и один товар.

### Создание базы и перенос данных

```sh
python -m db.import_json
```

Скрипт `db/import_json.py` создаёт таблицы по `sql/schema.sql`, очищает их и
переносит записи из JSON методом `executemany()`. Сначала добавляются клиенты и
товары, затем заказы, которые на них ссылаются. Скрипт можно запускать повторно.

`db/database.py` содержит `get_connection()`: соединение включает проверку внешних
ключей `PRAGMA foreign_keys = ON` и `row_factory = sqlite3.Row` для доступа к
полям по именам. Функции `fetch_all()` и `fetch_one()` выполняют запрос и
закрывают соединение.

### SQL-запросы

Проверенные запросы с комментариями хранятся в `sql/queries.sql`:

1. Список товаров (`ORDER BY`).
2. Список клиентов.
3. Товар по идентификатору (`WHERE`).
4. Товары не дороже заданной цены (`WHERE`).
5. Заказы в обработке (`WHERE`).
6. Заказы с клиентом, товаром и суммой (`JOIN`).
7. Полная информация о заказе (`JOIN` + `WHERE`).
8. Сводка: количество заказов, готовые, общая сумма (`COUNT`, `SUM`).
9. Минимальная, средняя и максимальная цена (`MIN`, `AVG`, `MAX`).
10. Заказы и сумма по клиентам (`LEFT JOIN` + `GROUP BY`).
11. Заказанное количество по товарам (`GROUP BY`).
12. Постоянные клиенты (`GROUP BY` + `HAVING`).

Запросы 1, 3, 4, 6–12 используются на страницах сайта. Значения от пользователя
и из URL передаются параметрами `?`, а не подставляются в текст запроса:

```python
fetch_all(
    'SELECT id, name, price FROM products WHERE price <= ? ORDER BY price',
    [max_price],
)
```

## Структура проекта

```text
order-tracking-system/
├── manage.py
├── main.py
├── requirements.txt
├── domain/
│   ├── clients.py
│   ├── products.py
│   ├── orders.py
│   └── common.py
├── infrastructure/
│   └── json_storage.py
├── db/
│   ├── database.py
│   └── import_json.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── console_app/
│   ├── input.py
│   └── menu.py
├── order_tracking/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   └── includes/
│       └── navigation.html
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   ├── views.py
│   └── urls.py
├── product_pages/
│   ├── templates/product_pages/
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── product_search.html
│   │   └── includes/product_card.html
│   ├── views.py
│   └── urls.py
├── web_orders/
│   ├── templates/web_orders/
│   │   ├── order_list.html
│   │   ├── order_detail.html
│   │   ├── statistics.html
│   │   └── includes/order_status.html
│   ├── views.py
│   └── urls.py
├── data/
│   ├── clients.json
│   ├── products.json
│   ├── orders.json
│   └── order_tracking.sqlite
└── tests/
    ├── test_project.py
    ├── test_web.py
    └── test_database.py
```

`main.py` оставлен короткой точкой запуска консольной версии. Он передаёт
управление в `console_app.menu`, поэтому корень проекта не содержит бизнес-логики.

## Установка и запуск веб-версии

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python -m db.import_json
python manage.py check
python manage.py runserver
```

После запуска откройте `http://127.0.0.1:8000/`.

## Запуск консольной версии

```sh
python main.py
```

## Тестирование и проверка кода

```sh
pytest -v
flake8 .
```

Тесты ПР3 проверяют объектную модель, операции над коллекциями и восстановление
связей из JSON. Тесты ПР5 проверяют основные страницы, динамические URL,
несуществующие идентификаторы и общую страницу 404. Тесты ПР6 проверяют
подключение базового шаблона, статических файлов и включаемого шаблона статуса.
Тесты ПР7 проверяют перенос данных из JSON в SQLite (в базе `:memory:`), поиск
товаров по цене и страницу статистики.

## Хранение данных

Данные находятся в файлах `data/clients.json`, `data/products.json` и
`data/orders.json`. При загрузке записи преобразуются в объекты. Заказ хранит
ссылки на объекты клиента и товара, а в JSON эти связи представлены полями
`client_id` и `product_id`.

Консольная версия по-прежнему работает с JSON. JSON-файлы — исходные данные для
базы SQLite: после их изменения базу нужно пересоздать командой
`python -m db.import_json`. Веб-интерфейс читает данные только из SQLite.

Django ORM для предметных данных пока не используется: запросы к SQLite
выполняются напрямую через `sqlite3`. Файл `db.sqlite3` нужен только встроенным
компонентам Django.

## Дальнейшее развитие

Следующие этапы — подключение базы к моделям Django и Django ORM, формы Django для
создания и редактирования данных и расширение веб-интерфейса.
