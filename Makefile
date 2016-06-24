.PHONY: run install clean

VENV_DIR ?= .env
PYTHON = $(VENV_DIR)/bin/python

run:
	clear
	$(PYTHON) imagefudge/image_fudge.py

init:
	rm -rf $(VENV_DIR)
	@$(MAKE) $(VENV_DIR)

clean:
	find . -iname "*.pyc" -delete
	find . -iname "*.pyo" -delete
	find . -iname "__pycache__" -delete

$(VENV_DIR):
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt