install:
	poetry install

lint:
	poetry run flake8 task_manager

shell:
	poetry shell

dev:
	python3 manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	python3 manage.py test

local:
	python3 manage.py makemessages -l ru

trans:
	python3 manage.py compilemessages

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate


