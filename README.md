# Визуальный планировщик ресурсов

REST API на FastAPI, которое помогает тимлидам студенческих проектов планировать загрузку команды и спринты на основе актуальных данных.

## Требования для запуска

Для запуска проекта на любом компьютере должны быть установлены:
* **Docker** и **Docker Desktop** (для Windows/macOS)
* **Docker Compose**

## Быстрый запуск

1. Создайте файл конфигурации проекта `.env` в корневой директории (все переменные указаны ниже)
2. Запустите сборку и старт всех контейнеров командой из терминала 
``` bash 
docker compose up --build
```

> Примечание: при первом холожном старте может потребоваться больше времени

## Как открыть документаци Swagger

После того, как контейнеры перейдут в статус успешной работы, откройте браузер и перейдите по ссылке:

👉 **[http://localhost/api/docs](http://localhost/api/docs)**

## Переменные окружения

| Название переменной | Тип    | Описание                                                   | Значение по умолчанию |
|---------------------|--------|------------------------------------------------------------|-----------------------|
| COMMON_PORT | int | Порт подключения | 8000 |
| DB__POSTGRES_SCHEME     | string | Схема подключения к PostgreSQL с асинхронным драйвером.    | postgresql+asyncpg    |
| DB__POSTGRES_HOST       | string | Хост локальной базы PostgreSQL.                            | localhost             |
| DB__POSTGRES_PORT       | int    | Порт подключения к PostgreSQL.                             | 5432                  |
| DB__POSTGRES_DB         | string | Имя базы данных для приложения.                            | capacity_planning     |
| DB__POSTGRES_USER       | string | Пользователь PostgreSQL с правами на базу.                 | postgres              |
| DB__POSTGRES_PASSWORD   | string | Пароль пользователя PostgreSQL.                            | postgres              |
| DB__ECHO             | bool   | Включить логирование SQL (True/False).                     | False                 |
| COMMON__FRONTEND_HOST | str | Хост фронтенда | http://localhost:5555 |
| COMMON__BACKEND_HOST | str | Хост фронтенда | http://localhost:5050 |
| AUTH__PRIVATE_KEY_PATH | string | Путь к секретному ключу для подписи JWT-токенов | private.pem |
| AUTH__PUBLIC_KEY_PATH | string | Путь к публичному ключу для расшифровки JWT-токенов | public.pem |
| AUTH__ALGORITHM           | string | Алгоритм шифрования JWT.                                   | RS256                 |
| AUTH__ACCESS_TOKEN_LIFETIME_SECONDS | int | Время жизни access-токена в секундах. | 600                  |
| AUTH__REFRESH_TOKEN_LIFETIME_SECONDS | int | Время жизни refresh-токена в секундах. | 3600                  |
| ROLE__ADMIN_EMAIL    | string | Email администратора | admin@example.com |
| ROLE__ADMIN_PASSWORD | string  | Пароль администратора | Admin123! |
| ROLE__ADMIN_FIRST_NAME | string | Имя администратора | Admin |
| ROLE__ADMIN_LAST_NAME | string | Фамилия администратора | Admin |
| ROLE__ADMIN_SKILLS | string | Скиллы администратора | System Admin |
| ROLE__ADMIN_ROLE_CODE | string | Код роли администратора | admin |
| ROLE__DEFAULT_USER_ROLE_CODE | string | Роль по умолчанию для новых пользователей | user |
| ROLE__BOOTSTRAP_ENABLED | Включить автоматическое создание ролей и администратора при запуске | true |
| LIMITER__DEFAULT_LIMITS| List[str] | Количество запросов пользователя на один ресурс в единицу времени | ["10/minute"] |
| LOGGING__FILE_NAME | str | Файл для логгирования | my_log.log|
| EMAIL__USERNAME | EmailStr | Почта отправителя | username@gmail.com |
| EMAIL__PASSWORD | SecretStr | Ключ приложения | secret_password |
| EMAIL__TITLE | str | Название письма | title |
| EMAIL__PORT | int | Порт подключения | 587 |
| EMAIL__SERVER | str | Хост подключения | smpt.gmail.com |
| EMAIL__FROM_NAME | str | Имя приложения | Capacity Planning|
| EMAIL__NOTIFICATION_LIFETIME_SECONDS | int | Время, в течение которого сервер пытается подключиться к почтовому сервиру | 3600 |
| EMAIL__TEMPLATES_DIR | str | Путь к шаблонам почтовых сообщений | templates |
| EMAIL__BASE_URL | str | Базовый url для ссылок подтверждения | http://locallost:8080/|

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


## Тестирование и авторизация 

В систему уже встроен скрипт создания первоначального администратора системы (параметры берутся из блока `ROLE__` вашего `.env')

1. Откройте Swagger UI.
2. Найдите блок **`auth`** и разверните эндпоинт **`POST /auth/login`**.
3. Нажмите **Try it out** и отправьте JSON со своими дефолтными данными.
4. Нажмите **Execute**. В случае успеха сервер вернет структуру с `access_token`.
5. Скопируйте значение полученного токена (без кавычек).
6. Поднимитесь в самый верх страницы Swagger UI, нажмите зеленую кнопку **Authorize**, вставьте токен в поле ввода и закройте модальное окно.

*Теперь вы авторизованы в системе с правами администратора и можете отправлять кастомные запросы к любым закрытым эндпоинтам.*



## Миграции (Alembic)
- Применить существующие миграции (первый запуск): `uv run alembic upgrade head`
- Создать новую миграцию (автогенерация по моделям): `uv run alembic revision --autogenerate -m "comment"`
- Откатить на один шаг: `uv run alembic downgrade -1`
- Алебмик берёт URL БД из `.env` (переменные из таблицы выше).

## Что внутри
- Асинхронное подключение к PostgreSQL через `postgresql+asyncpg` и SQLModel.
- Структура БД управляется миграциями Alembic, автосоздание таблиц при старте отключено.
- Все настройки берутся из переменных окружения (см. `.env.example`).


## Остановка проекта

Для корректной остановки всех контейнеров и очистки сетевых интерфейсов выполните:

```bash
docker compose down
```