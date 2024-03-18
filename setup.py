from setuptools import setup, find_packages

setup(
    name="lampctl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "phue==1.1"
    ],
    entry_points={
        "console_scripts": ["lampctl = lampctl:main"]
    }
)
