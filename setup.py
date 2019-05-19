# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests==2.22.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Nicholas Martin",
    author_email='drnicholasdmartin@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.7",
    ],
    description=("Model to be used as a recommendation engine for "
                 "people wishing to vote remain in the EU 2019 "
                 "elections in the UK"),
    entry_points={
        'console_scripts': [
            'eu2019model=eu2019model.recommend:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='eu2019model',
    name='eu2019model',
    packages=find_packages(include=['eu2019model']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/remainvoter/eu2019model',
    version='1.2.0',
    zip_safe=False,
)
