# Используем минимальный образ Python 3
FROM python:3.11.8-slim-bookworm

#Обновление списка пакетов. Установка необходимых компонентов/
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev --no-install-recommends

# Копируем наши зависимости
COPY ./requirements.txt /requirements.txt

# Устанавливаем требуемые пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ./app /app
WORKDIR /app

# Команда для запуска приложения с помощью uvicorn
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
