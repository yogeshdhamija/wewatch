ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# Settings:
REPO_NAME := wewatch_server

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell cd wewatch_server && pipenv --venv 2>&1 | if grep "$(REPO_NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

# Init dev environment
initserver:
	cd wewatch_server && pipenv install --dev && pipenv check

# Run redis server
runredis:
	cd wewatch_server && dependencies/redis-4.0.9/src/redis-server redis_db_options.conf

# Run server
runserver:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make initserver`.)
endif
	cd wewatch_server && pipenv run python src/server.py

# Remove virtualenv
cleanserver:
	cd wewatch_server && pipenv --rm
