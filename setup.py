from setuptools import setup

setup(
    name="lights",
    version="0.1.0",
    packages=["lights"],
    install_requires=[
        "phue==1.1"
    ],
    entry_points={
        "console_scripts": ["lights = lights.__main__:main"]
    }
)
