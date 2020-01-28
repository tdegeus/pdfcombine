
from setuptools import setup
from setuptools import find_packages

import re

filepath = 'pdfcombine/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
    name = 'pdfcombine',
    version = __version__,
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Script to combine PDF files (wrapper around GhostScript)',
    long_description = 'Script to combine PDF files (wrapper around GhostScript)',
    keywords = 'PDF, GhostScript',
    url = 'https://github.com/tdegeus/pdfcombine',
    packages = find_packages(),
    install_requires = ['docopt>=0.6.2', 'click>=4.0', 'pyyaml>=1.0'],
    entry_points = {
        'console_scripts': ['pdfcombine = pdfcombine.cli.pdfcombine:main']})
