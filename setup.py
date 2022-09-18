from setuptools import find_packages
from setuptools import setup

project_name = "pdfcombine"

setup(
    name=project_name,
    license="MIT",
    author="Tom de Geus",
    author_email="tom@geus.me",
    description="Script to combine PDF files (wrapper around GhostScript)",
    long_description="Script to combine PDF files (wrapper around GhostScript)",
    keywords="PDF, GhostScript",
    url=f"https://github.com/tdegeus/{project_name:s}",
    packages=find_packages(),
    use_scm_version={"write_to": f"{project_name}/_version.py"},
    setup_requires=["setuptools_scm"],
    install_requires=["docopt>=0.6.2", "click>=4.0", "pyyaml>=1.0"],
    entry_points={"console_scripts": ["pdfcombine = pdfcombine.cli.pdfcombine:main"]},
)
