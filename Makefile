# Makefile for Guará Contribution Workflows

.DEFAULT_GOAL := help

## Install all development and testing dependencies
install:
	python3.8 -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools
	. venv/bin/activate && pip install --upgrade -r test-requirements.txt
	pre-commit install

## Run the unit tests
test:
	tox -e unittest

## Run the linter check via tox
linter:
	tox -e linter

## Run full validation suite (all unit tests and linters via tox)
tox:
	tox

# Run all commands in sequence
all: install tox

## Display this help text
help:
	@echo "  make install             - Setup venv and install dependencies"
	@echo "  make test                - Run unit tests using pytest"
	@echo "  make linter              - Run linter via tox"
	@echo "  make tox                 - Run entire test and linter suite via tox"
	@echo "  make all                 - Run all commands"

.PHONY: help install install-pre-commit test test-tox linter tox
