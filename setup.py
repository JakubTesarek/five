"""Install lmc-radlib and dependencies."""

import sys

from setuptools import setup


def get_package_version():
    number_of_arguments = len(sys.argv)
    optional_version_parameter = sys.argv[-1]

    if optional_version_parameter.startswith('--version'):
        version = optional_version_parameter.split("=")[1]
        sys.argv = sys.argv[0:number_of_arguments - 1]
    else:
        with open('VERSION', 'rt') as version_file:
            version = version_file.read().strip()

    return version


def main():
    setup(
        name='five-in-row',
        version=get_package_version(),
        python_requires='>=3.7',
        description='Framework for playing piskvorky.jobs.cz',
        long_description='',
        url='https://github.com/JakubTesarek/five',
        author='Jakub Tesárek',
        author_email='jakub@tesarek.me',
        license='unlicensed',
        include_package_data=True,
        packages=['five_in_row'],
        install_requires=[
            'requests',
            'numpy'
        ],
        extras_require={
            'dev': [
                'setuptools',
                'wheel',
                'pytest',
                'pytest-cov',
                'pytest-mock',
                'requests-mock',
                'mypy',
                'flake8',
                'flake8-colors',
                'flake8-eradicate',
                'flake8-print',
                'flake8-todo',
                'twine'
            ],
        }
    )


if __name__ == '__main__':
    main()
