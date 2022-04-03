from setuptools import setup, find_packages

setup(
    name="lights",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "phue==1.1"
    ],
    entry_points={
        "console_scripts": ["lights = lights:main"]
    }
)
