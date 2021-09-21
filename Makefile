.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
.SILENT: clean, test

SLUG := zemmourify
DOCKER_IMAGE_LOCAL := "${SLUG}-local"
DOCKER_IMAGE_PROD := ${SLUG}

quiet := 1
no_lint := 1

help:
	@echo "${GREEN}-----------------------------------------------------------------${RESET}"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	@rm -fr build/ dist/ .eggs/ public/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

	@rm -fr .coverage cov-report .pytest_cache

lint:  ## check for style 
	flake8 ${SLUG} tests
	black ${SLUG} tests --check
	isort ${SLUG} tests --check-only
	mypy ${SLUG} tests

test:  ## run tests and coverage quickly with the default Python
	@if [ "${no_lint}" != "1" ]; then make lint; fi
	pytest

open-cov:  ## open overage report
	@open cov-report/htmlcov/index.html


install-dev: ## install the package for developement as symlink
	make clean
	PIP_QUIET=${quiet} flit install --deps develop --symlink

install: ## install the package to the active Python's site-packages
	make clean
	PIP_QUIET=${quiet} flit install --deps production

init: ## setup the dev enviroment
	if [ ! -d .git ]; then git init; fi
	if [ -f .vscode/settings.tpl.json ]; then cp .vscode/settings.tpl.json .vscode/settings.json; fi
	if [ -f .env.example ]; then cp .env.example .env; fi
	PIP_QUIET=${quiet} pip install flit
	make install-dev
	make test
	pre-commit install --hook-type commit-msg
	make help

docker-build:  ## [DEV  ] build docker image without downloading the model
	@echo "${GREEN}Building image ${DOCKER_IMAGE_LOCAL} ${RESET}"
	docker build -t ${DOCKER_IMAGE_LOCAL} \
		--build-arg env="DEV" \
		.


docker-exec: ## [DEV  ] run cmd inside dev docker
	docker run --rm \
		--mount type=bind,source="$(shell pwd)",target=/task \
		--entrypoint "/bin/bash" \
		$$args1 ${args} \
		${TTY} ${DOCKER_IMAGE_LOCAL} \
		-c "${cmd}"


docker-test:  ## [DEV  ] run test inside docker
	make docker-exec cmd="make test no_lint=1"


docker-prod-build:  ## [PROD ] build docker image with the model downloaded inside
	@echo "${GREEN}Building image ${DOCKER_IMAGE_PROD} ${RESET}"
	docker build -t ${DOCKER_IMAGE_PROD} \
		--build-arg env=PROD \
		.


docker-prod-test:  ## [PROD ] run test inside docker prod
	docker run --rm \
	--mount type=bind,source="$(shell pwd)"/tests,target=/task/tests \
  --entrypoint "/bin/bash" \
	${TTY} ${DOCKER_IMAGE_PROD} \
	-c "PIP_QUIET=${quiet} FLIT_ROOT_INSTALL=1 flit install --deps production --extra test && make test no_lint=1"


# Show line with ## in help
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		target = "${PURPLE}" + target + "${RESET}"
		print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

# Define standard colors
ifneq (, $(shell which tput))
BLACK        := $(shell tput -Txterm setaf 0)
RED          := $(shell tput -Txterm setaf 1)
GREEN        := $(shell tput -Txterm setaf 2)
YELLOW       := $(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
PURPLE       := $(shell tput -Txterm setaf 5)
BLUE         := $(shell tput -Txterm setaf 6)
WHITE        := $(shell tput -Txterm setaf 7)

RESET := $(shell tput -Txterm sgr0)
endif

# To be override in system without tty
TTY := "-it"

# darwin or linux
OS_NAME := $(shell uname -s | tr A-Z a-z)