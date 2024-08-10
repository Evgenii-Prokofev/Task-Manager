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
	poetry run python3 manage.py test

local:
	python3 manage.py makemessages -l ru

trans:
	python3 manage.py compilemessages

migrations:
	python3 manage.py makemigrations

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

migrate:
	python3 manage.py migrate


