from setuptools import setup

setup(
    name = 'pdfcombine',
    description = 'Script of combine PDF files (wrapper around GhostScript)',
    long_description = 'Script of combine PDF files (wrapper around GhostScript)',
    keywords = 'PDF, GhostScript',
    version = '0.4.0',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    url = 'https://github.com/tdegeus/pdfcombine',
    entry_points = {
        'console_scripts': ['pdfcombine = pdfcombine:main']}
)
