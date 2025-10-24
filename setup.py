# setup.py
from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read LICENSE
with open("LICENSE", "r", encoding="utf-8") as f:
    license_text = f.read()

setup(
    name="finaTSE",
    version="0.1.2",
    author="Mehdi Zallaghi",
    author_email="mmzallaghi@egmail.com",
    description="Access Tehran Stock Exchange (TSE) market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mzallaghi4/finaTSE",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "beautifulsoup4>=4.9.0",
    ],
    python_requires=">=3.7",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="tse tehran stock exchange iran finance market data",
)
