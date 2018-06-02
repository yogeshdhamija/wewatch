ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# Settings:
REPO_NAME := wewatch-server

# VENV is 1 if virtualenv exists, otherwise 0:
VENV := $(shell cd wewatch-server && pipenv --venv 2>&1 | if grep "$(REPO_NAME)" > /dev/null; then echo '1'; else echo '0'; fi;)

# Build angular output to server directory
buildclient:
	cd wewatch-client && ng build --prod --build-optimizer --base-href=static/ && cp -r dist/wewatch-client ../wewatch-server/client_build

# Init dev environment
initserver:
	cd wewatch-server && pipenv install --dev && pipenv check
initclient:
	cd wewatch-client && yarn

# Run redis server
runredis:
	cd wewatch-server && dependencies/redis-4.0.9/src/redis-server redis_db_options.conf

# Run server
runserver:
ifeq "$(VENV)" "0"
	$(error It looks like you don't have a virtual environment. Please run `make initserver`.)
endif
	cd wewatch-server && pipenv run python src/server.py

# Remove virtualenv
cleanserver:
	cd wewatch-server && pipenv --rm
