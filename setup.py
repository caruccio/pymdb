#!/usr/bin/env python
# This file stolen from https://github.com/kennethreitz/samplemod
# coding: utf-8

from setuptools import setup, find_packages

with open('README.md') as f:
	readme = f.read()

with open('LICENSE') as f:
	license = f.read()

setup(
	name='pymdb',
	version='0.0.1',
	description='Python module to retrieve IMDB movie info from http://www.imdbapi.org',
	long_description=readme,
	author='Mateus Caruccio',
	author_email='mateus@caruccio.com',
	url='https://github.com/caruccio/pymdb',
	license=license,
	packages=find_packages(exclude=('tests', 'docs'))
)

