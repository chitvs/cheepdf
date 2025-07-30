from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cheepdf",
    version="1.0.0",
    author="Alessandro Chitarrini",
    license="AGPL-3.0-or-later",
    description="A simple PDF annotation remover",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chitvs/cheepdf",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "PyMuPDF>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "cheepdf=cheepdf.cli:main",
        ],
    },
)
