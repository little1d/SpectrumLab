"""
Setup script for SpectrumLab package.
This allows the package to be installed in development mode.
"""

from setuptools import setup, find_packages

setup(
    name="spectrumlab",
    version="0.0.1",
    description="Comprehensive toolkit for spectroscopy deep learning",
    packages=find_packages(),
    install_requires=[
        "dotenv>=0.9.9",
        "openai>=1.93.0",
    ],
    python_requires=">=3.10",
) 