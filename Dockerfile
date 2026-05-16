# Используем ту же версию Python, что и ваша uv локально
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Указываем корень контейнера как основной путь для поиска модулей
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir uv

# Копируем конфигурации зависимостей
COPY pyproject.toml uv.lock .python-version ./

# Синкаем зависимости (uv создаст /app/.venv)
RUN uv sync --frozen --no-dev

# Копируем весь остальной код проекта (включая папку app и alembic)
COPY . .

# Создаем скрипт для запуска
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
/app/.venv/bin/python -m alembic upgrade head\n\
echo "Starting application..."\n\
# Запуск uvicorn через виртуальное окружение\n\
exec /app/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Запускаем через скрипт
CMD ["/app/start.sh"]