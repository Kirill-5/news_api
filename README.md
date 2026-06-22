# News API

Асинхронный парсер RSS-лент с кэшированием в Redis и хранением в PostgreSQL.


## Что нового

В этом проекте, по сравнению с предыдущими:

- Асинхронное выполнение (async/await, aiohttp)
- Парсинг RSS-лент (feedparser)
- Кэширование через Redis (fastapi-cache)
- Миграции через Alembic (вместо create_all)


## Что умеет

- Парсит RSS-ленту по указанному URL
- Сохраняет новости в PostgreSQL (без дубликатов)
- Кэширует результат в Redis на 5 минут
- Отдаёт список новостей через FastAPI
- Миграции через Alembic

## Запуск через Docker Compose

```bash
docker-compose up --build
```

# Локальный запуск (без Docker)

## Установить зависимости ,  поднять PostgreSQL и Redis
```
poetry install
docker run --name postgres_news -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec -it postgres_news psql -U postgres -c "CREATE DATABASE news_db"
docker run --name redis_cache -d -p 6379:6379 redis
```

## Применить миграции и запустить
```
alembic upgrade head
poetry run uvicorn app.main:app --reload
```

# API
GET /news
Параметры:
url — ссылка на RSS-ленту (обязательно)

Пример запроса:
```
GET /news?url=https://habr.com/ru/rss/all/all/
```

# Кэширование
- Первый запрос парсит ленту и сохраняет в БД + Redis
- Повторные запросы в течение 5 минут возвращают данные из Redis
- Через 5 минут кэш сбрасывается и при следующем запросе данные обновляются


# Структура проекта
```
news_api/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── news.py        # эндпоинты
│   ├── core/
│   │   └── config.py           # настройки
│   ├── db/
│   │   └── database.py         # подключение к БД
│   ├── models/
│   │   └── news.py             # SQLAlchemy модель
│   ├── schemas/
│   │   └── news.py             # Pydantic схема
│   ├── services/
│   │   └── parser.py           # парсинг + сохранение
│   └── main.py                 # точка входа
├── alembic/                    # миграции
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md
```


# Технологии
Python 3.12
FastAPI
PostgreSQL + SQLAlchemy
Redis + fastapi-cache
Alembic
Docker / Docker Compose
