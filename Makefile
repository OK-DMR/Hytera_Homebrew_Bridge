.PHONY: test
test:
	python -m coverage erase
	PYTHONPATH=. pytest -vrP --cov-report=term-missing --cov=okdmr.hhb --cov-report=xml

clean:
	git clean -xdff
