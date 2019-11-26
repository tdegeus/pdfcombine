from setuptools import setup

setup(
    name = 'pdfcombine',
    version = '0.4.1',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Script of combine PDF files (wrapper around GhostScript)',
    long_description = 'Script of combine PDF files (wrapper around GhostScript)',
    keywords = 'PDF, GhostScript',
    url = 'https://github.com/tdegeus/pdfcombine',
    packages = ['pdfcombine'],
    entry_points = {
        'console_scripts': ['pdfcombine = pdfcombine:main']}
)
