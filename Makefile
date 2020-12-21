.PHONY: tests
default: tests


build: clean
	python setup.py sdist bdist_wheel

clean:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf htmlcov .coverage
	rm -rf build dist
	
lint: clean
	flake8 .
	mypy .

test: clean
	py.test tests/* -s \
		--cov five_in_row \
		--cov-report html \
		--cov-report term \
		--cov-fail-under=100

tests: clean lint test