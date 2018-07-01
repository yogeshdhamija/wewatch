ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# Settings:
NAME := wewatch

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell cd $(NAME) && pipenv --venv 2>&1 | if grep "$(NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

init:
	cd $(NAME) && pipenv install --dev && pipenv check

redis:
	cd $(NAME) && dependencies/redis-4.0.9/src/redis-server redis_db_options.conf

server:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make initserver`.)
endif
	cd $(NAME) && pipenv run python src/server.py

clean:
	cd $(NAME) && pipenv --rm
