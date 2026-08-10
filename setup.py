#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="graphene-django-optimizer",
    version="0.9.1",
    author="Tomás Fox",
    author_email="tomas.c.fox@gmail.com",
    description="Optimize database access inside graphene queries.",
    license="MIT",
    keywords="graphene django optimizer optimize graphql query prefetch select related",
    url="https://github.com/tfoxy/graphene-django-optimizer",
    packages=["graphene_django_optimizer"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
    ],
)
