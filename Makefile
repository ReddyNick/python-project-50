install:
	poetry install

selfcheck:
	poetry check

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

lint:
	poetry run flake8 gendiff

check: selfcheck test lint

build: check
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pipx install --force dist/*.whl

.PHONY: install test lint selfcheck check build