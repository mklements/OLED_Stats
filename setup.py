"""Setup for smartrack-pi"""

from setuptools import find_packages, setup


def _readme():
    with open("README.md", encoding="utf-8") as file:
        return file.read()


setup(
    name="smartrack-pi",
    version="1.0.0",
    description="Pi Oled config",
    long_description=_readme(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    url="http://github.com/ctus-dev/smartrack-pi",
    author="Craig Mitchell",
    author_email="craig.mitchell@ctus.com",
    license="GNU",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
