#!/usr/bin/env python3
import os

from setuptools import find_packages, setup

import elkcli.constants as const

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="elkcli",
    version=const.__version__,
    author="Gena Mirson",
    author_email="mirsongena@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["elkcli=elkcli.elkcli:cli.main"]},
    install_requires=[
        "rich",
        "elasticsearch",
        "prompt_toolkit",
    ],
    python_requires=">=3.7",
    classifiers=[ ],
    keywords="",
)
