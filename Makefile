lint: 
	poetry run flake8 page_analyzer tests

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml


selfcheck:
	poetry check

check: selfcheck lint test 

build: check
	poetry build

push:
	python3 -m pip install dist/python_project_83-0.1.0-py3-none-any.whl --force-reinstall