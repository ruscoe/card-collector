# Makefile for Card Collector Docker development

.PHONY: build up down logs shell test

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose run --rm web /bin/sh

psql:
	docker compose exec db psql -U postgres -d card_collector

requirements:
	python -m pip install --upgrade pip
	python -m pip install -r api/requirements.txt
