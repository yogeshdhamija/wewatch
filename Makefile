# Settings:
NAME := wewatch

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell pipenv --venv 2>&1 | if grep "$(NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

init:
	pipenv install --dev && pipenv check

redis:
	dependencies/redis-4.1.0/src/redis-server redis_db_options.conf

run:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make initserver`.)
endif
	pipenv run python src/server.py

clean:
	pipenv --rm
