#!/usr/bin/env python
"""
distutils setup (setup.py)

This gets a bit of package info from __pkginfo__.py file
"""
# Get the required package information
from __pkginfo__ import (
    author,
    author_email,
    classifiers,
    install_requires,
    license,
    long_description,
    modname,
    py_modules,
    short_desc,
    VERSION,
    web,
    zip_safe,
)

__import__("pkg_resources")
from setuptools import setup, find_packages

packages = find_packages()

setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=short_desc,
    install_requires=install_requires,
    license=license,
    long_description=long_description,
    name=modname,
    packages=packages,
    py_modules=py_modules,
    test_suite="nose.collector",
    url=web,
    version=VERSION,
    zip_safe=zip_safe,
)
