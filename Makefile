lint: 
	poetry run flake8 page_analyzer tests

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml


selfcheck:
	poetry check

check: selfcheck lint test 

build: check
	poetry build

push:
	python3 -m pip install dist/python_project_83-0.1.0-py3-none-any.whl --force-reinstall

dev:
	poetry run flask --app page_analyzer:app run
	
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app