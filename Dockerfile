FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем poetry и зависимости
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем код
COPY . .

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]