"""
This setup.py is solely used to install the package in development mode
by running from the server/ dir:

```
pip install -e .
```
"""

from setuptools import setup, find_packages

setup(
    name='architext',
    version='0.0.1',
    install_requires=[
        'setuptools'
    ],
    packages=find_packages()
)