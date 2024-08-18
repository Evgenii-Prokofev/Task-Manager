### Hexlet tests and linter status:
[![Actions Status](https://github.com/Evgenii-Prokofev/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Evgenii-Prokofev/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/43174731d535a701fa51/maintainability)](https://codeclimate.com/github/Evgenii-Prokofev/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/43174731d535a701fa51/test_coverage)](https://codeclimate.com/github/Evgenii-Prokofev/python-project-52/test_coverage)
### Готовое к использованию приложение, доступно по следующему адресу:
https://task-manager-evgenii.onrender.com/

**"Task Manager"** - Веб-приложение для управления задачами, созданное на основе Python и Django framework. Оно позволяет ставить задачи, назначать исполнителей и изменять их статусы. Для работы с системой требуется регистрация и аутентификация.
### Перед установкой:
Для установки и запуска проекта вам потребуется Python версии 3.10 и выше, инструмент для управления зависимостями Poetry.

Перед началом использования проекта убедитесь, что вышеописанные утилиты установлены на вашем устройстве. В противном случае используйте официальную документацию для установки.
### Установка:
1. Склонируйте репозиторий с проектом на ваше локальное устройство:

```
git clone git@github.com:Evgenii-Prokofev/python-project-52.git
```
2. Перейдите в директорию проекта:

```
cd python-project-52
```
3. Установите необходимые зависимости с помощью Poetry:

```
poetry install
```
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки:

```
SECRET_KEY=ваш_ключ
DATABASE_URL=ваше_значение_External_Database_URL_или_используйте_локальное_подключение
DEBUG=False
```
5. Выполните команды:

```
make migrations
make migrate
```
  
### Использование:
Для запуска сервера в продакшн среде с помощью Gunicorn выполните команду:

```
make start
```
По умолчанию сервер будет доступен по адресу http://0.0.0.0:8000.

Также можно запустить сервер локально в режиме разработки с активным отладчиком:

```
make dev
```
Сервер для разработки будет доступен по адресу http://127.0.0.1:8000.

Проект можно использовать онлайн (например с помощью стороннего сервиса render.com). 
Следуйте инструкциям с официального сайта для добавления веб-сервиса и онлайн базы данных. 
Не забывайте про использования переменных окружения.
