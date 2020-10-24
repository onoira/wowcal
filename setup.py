#!/usr/bin/env python3

import os
from setuptools import find_packages, setup

# Package meta-data.
PACKAGE = 'wowcal'

# What packages are required for this module to be executed?
REQUIRED = [
    'click~=7.1.2', 'pyyaml>=5.3.1',
]

# What packages are optional?
EXTRAS = {
    'Validation': ['jsonschema'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, PACKAGE.lower(), '__version__.py')) as fp:
    exec(fp.read(), about)

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as fp:
        long_description = '\n' + fp.read()
except FileNotFoundError:
    long_description = about['__description__']

# Where the magic happens:
setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    python_requires=about['PYTHON_REQUIRES'],
    url=about['__url__'],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    entry_points={
        'console_scripts': ['wowcal=wowcal.__main__:main.main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT'
)
