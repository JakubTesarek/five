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
	flake8 five/*
	mypy  five/*

test: clean
	py.test tests/* -s \
		--cov five \
		--cov-report html \
		--cov-report term \
		--cov-fail-under=100

tests: clean lint test