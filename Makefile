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


