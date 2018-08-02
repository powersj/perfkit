PYTHON = python3

.PHONY: clean test venv

clean:
	rm -rf .tox .eggs *.egg-info build dist venv
	@find . -regex '.*\(__pycache__\|\.py[co]\)' -delete

test:
	tox

venv:
	$(PYTHON) -m virtualenv -p /usr/bin/$(PYTHON) venv
	venv/bin/pip install -Ur requirements.txt
	@echo "Now run the following to activate the virtual env:"
	@echo ". venv/bin/activate"
