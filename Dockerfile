# Используем официальный образ Python как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями (requirements.txt) в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Указываем переменную окружения для Django, чтобы не запускать сервер в режиме отладки
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Открываем порт, который будет использовать Django
EXPOSE 8000
