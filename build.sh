#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Установка зависимостей с помощью poetry
poetry install

# Сбор статических файлов
python3 manage.py collectstatic --no-input

# Применение миграций
python3 manage.py migrate

# Компиляция сообщений для локалей
python3 manage.py compilemessages