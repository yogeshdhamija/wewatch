ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# Settings:
REPO_NAME := wewatch

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell pipenv --venv 2>&1 | if grep "$(REPO_NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

# Init dev environment
init:
	pipenv install --dev
	pipenv check

# Run server
runserver:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make init`.)
endif
	PYTHONPATH=src/ pipenv run python src/server/server.py

# Remove virtualenv
clean:
	pipenv --rm
