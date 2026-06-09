SHELL := /bin/bash

ENV_NAME := kb-refactor
YML_FILE := kb-refactor.yml

TARGET ?= .

PYTHON := micromamba run -n $(ENV_NAME) python
PIP := micromamba run -n $(ENV_NAME) pip

PHONY_TARGETS := \
	help \
	info \
	create \
	update \
	install \
	run \
	dry \
	check \
	verbose \
	stats \
	lint \
	build \
	upload \
	remove \
	deep-clean

.PHONY: $(PHONY_TARGETS)

help:
	@echo ""
	@echo "Environment"
	@echo "-----------"
	@echo "  create"
	@echo "  update"
	@echo "  remove"
	@echo ""
	@echo "Development"
	@echo "-----------"
	@echo "  install"
	@echo "  run"
	@echo "  dry"
	@echo "  check"
	@echo "  verbose"
	@echo "  stats"
	@echo "  lint"
	@echo ""
	@echo "Packaging"
	@echo "---------"
	@echo "  build"
	@echo "  upload"
	@echo ""
	@echo "Maintenance"
	@echo "-----------"
	@echo "  info"
	@echo "  deep-clean"
	@echo ""

info:
	@echo ""
	@echo "ENV_NAME = $(ENV_NAME)"
	@echo "YML_FILE = $(YML_FILE)"
	@echo "TARGET   = $(TARGET)"
	@echo ""
	@echo "Micromamba environments:"
	@micromamba env list || true
	@echo ""

create:
	micromamba env create -f $(YML_FILE)

update:
	micromamba env update \
		-f $(YML_FILE) \
		--prune

install:
	$(PIP) install -e .

run:
	micromamba run -n $(ENV_NAME) \
		kb_refactor $(TARGET)

dry:
	micromamba run -n $(ENV_NAME) \
		kb_refactor $(TARGET) --dry-run

check:
	micromamba run -n $(ENV_NAME) \
		kb_refactor $(TARGET) --check

verbose:
	micromamba run -n $(ENV_NAME) \
		kb_refactor $(TARGET) --verbose

stats:
	micromamba run -n $(ENV_NAME) \
		kb_refactor $(TARGET) --stats

lint:
	micromamba run -n $(ENV_NAME) \
		ruff check src

build:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

	$(PYTHON) -m build

upload:
	$(PYTHON) -m twine upload dist/*

remove:
	micromamba env remove \
		-n $(ENV_NAME) \
		-y

deep-clean:
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache

	find . -type d -name "__pycache__" -exec rm -rf {} +

	find . \
		-type d \
		-name "*.egg-info" \
		-exec rm -rf {} +

	find . \
		-type d \
		-name ".ipynb_checkpoints" \
		-exec rm -rf {} +