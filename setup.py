from setuptools import setup

setup(
    name="lights",
    version="0.1.0",
    packages=["lights"],
    entry_points={
        "console_scripts": ["lights = lights.__main__:main"]
    }
)
