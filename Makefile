.PHONY: help install clear lint run-dev run-prod
#SHELL := /bin/bash
PYTHON_PATH_answers_service := /home/olha/repos/4m-fields-service/fields_service
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
	. /home/olha/repos/4m-fields-service/venv/bin/activate; \
	pip install setuptools --upgrade --ignore-installed --user
	pip install pip --upgrade --ignore-installed --user
	pip install -r requirements.txt --user;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

dev-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_answers_service);\
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="development"; \
	 flask run --port=5053;


prod-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_answers_service); \
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="production"; \
	 flask run --port=5053;

lint:
	pylint setup.py
	pylint fields_service/