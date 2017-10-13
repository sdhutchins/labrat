#!/usr/bin/env python3

""" This is the setup.py script for setting up the package and fulfilling any
necessary requirements.
"""

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

# Set the home path of the setup script/package
home = path.abspath(path.dirname(__file__))
name = 'labrat'


def readme():
    """Get the long description from the README file."""
    with open(path.join(home, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name=name,
    author='Shaurita Hutchins',
    description="A package of helpful guis and functions to improve reproducibility for genetics/psychiatry related labs.",
    version='0.1',
    long_description=readme(),
    url='https://github.com/sdhutchins/labrat',
    license='',
    keywords='science lab pyschiatry math filemanagement',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    # Packages will be automatically found if not in this list.
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['']
    },
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose']
)
