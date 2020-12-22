.PHONY: tests
default: tests


build: clean
	python setup.py sdist bdist_wheel

run.examples:
	jupyter notebook examples 

clean:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	rm -rf .mypy_cache
	rm -rf *.egg-info
	rm -rf .pytest_cache .benchmarks
	rm -rf htmlcov .coverage
	rm -rf build dist
	
check.lint: clean
	flake8 .

check.typing:
	mypy .

check.tests: clean
	py.test tests/* -s \
		--cov five_in_row \
		--cov-report html \
		--cov-report term \
		--cov-fail-under=100

check.all: clean check.lint check.typing check.tests