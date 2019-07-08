.PHONY: help install clear lint dev-env prod-env
#SHELL := /bin/bash
PYTHON_PATH_field_service := /home/olha/repos/fields-service-repo/fields_service
.DEFAULT: help
help:
	@echo "make install"
	@echo "       creates venv and installs requirements"
	@echo "make run-dev"
	@echo "       run project in dev mode"
	@echo "make run-prod"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make clear"
	@echo "       deletes venv and .pyc files"

install:
	python3 -m venv venv
	. /home/olha/repos/fields-service-repo/venv/bin/activate; \
	pip install setuptools --upgrade --ignore-installed --user
	pip install pip --upgrade --ignore-installed --user
	pip install -r requirements.txt --user;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

dev-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_fields_service);\
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="development"; \
	 flask run --port=5053;


prod-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_fields_service); \
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="production"; \
	 flask run --port=5053;

lint:
	pylint setup.py fields_service/