#!/usr/bin/env python
from sonq import __VERSION__

long_description = ""

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    pass

sdict = {
    'name': 'sonq',
    'version': __VERSION__,
    'packages': ['sonq'],
    'zip_safe': False,
    'install_requires': ['six', 'pymongo'],
    'author': 'Lichun',
    'long_description': long_description,
    'url': 'https://github.com/socrateslee/sonq',
    'entry_points': {
        'console_scripts': [
            'sonq=sonq.cmd:main',
        ]
    },
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == '__main__':
    setup(**sdict)
