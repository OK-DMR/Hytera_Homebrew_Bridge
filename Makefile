.PHONY: test
test:
	python -m coverage erase
	pytest -vrP --cov-report=term-missing --cov=okdmr.hhb --cov-report=xml

clean:
	git clean -xdff

release:
	python3 -m build . --sdist --wheel
