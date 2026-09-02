.PHONY: install dev test

install:
	pip install -r requirements.txt

dev:
	fastapi dev app/main.py

test:
	pytest -q
