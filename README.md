# Визуальный планировщик ресурсов

REST API на FastAPI, которое помогает тимлидам студенческих проектов планировать загрузку команды и спринты на основе актуальных данных.

## Быстрый старт
1. Убедитесь, что локально запущен PostgreSQL и доступен по данным из `.env`.
2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install uv
   uv sync
   ```
3. Скопируйте пример переменных окружения и при необходимости отредактируйте:
   ```bash
   copy .env.example .env
   ```
4. Запустите приложение:
   ```bash
   uv run fastapi dev app/main.py
   ```
   Таблицы создадутся автоматически при старте приложения.

## Переменные окружения

| Название переменной | Тип    | Описание                                                   | Значение по умолчанию |
|---------------------|--------|------------------------------------------------------------|-----------------------|
| DB_POSTGRES_SCHEME     | string | Схема подключения к PostgreSQL с асинхронным драйвером.    | postgresql+asyncpg    |
| DB_POSTGRES_HOST       | string | Хост локальной базы PostgreSQL.                            | localhost             |
| DB_POSTGRES_PORT       | int    | Порт подключения к PostgreSQL.                             | 5432                  |
| DB_POSTGRES_DB         | string | Имя базы данных для приложения.                            | capacity_planning     |
| DB_POSTGRES_USER       | string | Пользователь PostgreSQL с правами на базу.                 | postgres              |
| DB_POSTGRES_PASSWORD   | string | Пароль пользователя PostgreSQL.                            | postgres              |
| DB_ECHO             | bool   | Включить логирование SQL (True/False).                     | False                 |
| AUTH_PRIVATE_KEY_PATH | string | Путь к секретному ключу для подписи JWT-токенов | private.pem |
| AUTH_PUBLIC_KEY_PATH | string | Путь к публичному ключу для расшифровки JWT-токенов | public.pem |
| AUTH_ALGORITHM           | string | Алгоритм шифрования JWT.                                   | RS256                 |
| AUTH_ACCESS_TOKEN_LIFETIME_SECONDS | int | Время жизни access-токена в секундах. | 600                  |
| AUTH_REFRESH_TOKEN_LIFETIME_SECONDS | int | Время жизни refresh-токена в секундах. | 3600                  |
| AUTH_ADMIN_EMAIL | Email администратора | admin@example.com |
| AUTH_ADMIN_PASSWORD | Пароль администратора | Admin123! |
| AUTH_ADMIN_FIRST_NAME | Имя администратора | Admin |
| AUTH_ADMIN_LAST_NAME | Фамилия администратора | User |
| AUTH_ADMIN_ROLE_CODE | Код роли администратора | admin |
| AUTH_DEFAULT_USER_ROLE_CODE | Роль по умолчанию для новых пользователей | user |
| BOOTSTRAP_ENABLED | Включить автоматическое создание ролей и администратора при запуске | true |

## Генерация JWT ключей (для асимметричного шифрования RS256)

1. Сгенерируйте приватный ключ (минимум 2048 бит):
```bash
   openssl genrsa -out private.pem 2048
```
2. Извлеките публичный ключ:
``` bash 
   openssl rsa -in private.pem -pubout -out public.pem
```

⚠️ **Требования к ключам:**
- Длина ключа: минимум 2048 бит (что соответствует >32 символам в base64)
- Формат: PEM
- Приватный ключ должен быть защищен и не попадать в репозиторий


## Миграции (Alembic)
- Применить существующие миграции (первый запуск): `uv run alembic upgrade head`
- Создать новую миграцию (автогенерация по моделям): `uv run alembic revision --autogenerate -m "comment"`
- Откатить на один шаг: `uv run alembic downgrade -1`
- Алебмик берёт URL БД из `.env` (переменные из таблицы выше).

## Что внутри
- Асинхронное подключение к PostgreSQL через `postgresql+asyncpg` и SQLModel.
- Структура БД управляется миграциями Alembic, автосоздание таблиц при старте отключено.
- Все настройки берутся из переменных окружения (см. `.env.example`).
