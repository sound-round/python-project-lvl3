build:
	poetry build

package_install:
	pip install --user dist/*.whl

force-package-install:
	pip install --force-reinstall --user dist/*.whl

install:
	poetry install

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page-loader

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page-loader --cov-report xml tests/