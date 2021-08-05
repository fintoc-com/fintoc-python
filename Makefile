# Env stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

.PHONY: build-env
build-env:
	python3 -m venv .venv
	poetry run pip install --upgrade pip
	poetry run poetry install

# Tests
.PHONY: tests
tests:
	poetry run pytest tests

# Passive linters
.PHONY: black
black:
	poetry run black fintoc tests --check

.PHONY: flake8
flake8:
	poetry run flake8 fintoc tests

.PHONY: isort
isort:
	poetry run isort fintoc tests --profile=black --check

.PHONY: pylint
pylint:
	poetry run pylint fintoc

# Aggresive linters
.PHONY: black!
black!:
	poetry run black fintoc tests

.PHONY: isort!
isort!:
	poetry run isort fintoc tests --profile=black

# Utilities
.PHONY: bump!
bump!:
	sh scripts/bump.sh $(filter-out $@,$(MAKECMDGOALS))

# Receive args (use like `$(filter-out $@,$(MAKECMDGOALS))`)
%:
	@:
