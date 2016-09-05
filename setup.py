#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'gurobipy>=6.5.2'
]

setup(
    name='minpower',
    version='1.0',
    description='Re-implemented version of my masters project.',
    author='Billy Tang',
    author_email='billy.tang164@gmail.com',
    url='https://github.com/billy164/master-research',
    install_requires=requires
)
