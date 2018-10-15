# Settings:
NAME := wewatch
REDIS_SERVER_EXECUTABLE := redis-server

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell pipenv --venv 2>&1 | if grep "$(NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

init:
	pipenv --python=2.7
	pipenv install --dev && pipenv check

redis:
	$(REDIS_SERVER_EXECUTABLE) redis_db_options.conf

run:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make init`.)
endif
	cd src && pipenv run python server.py

clean:
	pipenv --rm
