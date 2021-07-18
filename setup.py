#!/usr/bin/env python3
import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="hytera-homebrew-bridge",
    description="Connect Hytera IPSC repeater to MMDVM system such as HBlink, DMRGateway",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/OK-DMR/Hytera_Homebrew_Bridge",
    author="Marek Sebera",
    author_email="marek.sebera@gmail.com",
    license="AGPL-3.0",
    version="2021.2",
    packages=[
        "hytera_homebrew_bridge",
        "hytera_homebrew_bridge.kaitai",
        "hytera_homebrew_bridge.lib",
        "hytera_homebrew_bridge.tests",
    ],
    zip_safe=False,
    scripts=["bin/hytera-homebrew-bridge.py"],
    keywords="mmdvm dmr hytera repeater ham radio repeater",
    python_requires="~=3.7",
    install_requires=[
        "configparser>=5.0.1",
        "kaitaistruct>=0.9",
        "puresnmp>=1.10.2",
        "asyncio>=3.4.3",
        "dmr_utils3>=0.1.29",
        "bitarray>=1.6.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Environment :: Console",
        "Topic :: Communications :: Ham Radio",
        "Operating System :: POSIX :: Linux",
        "Typing :: Typed",
        "Framework :: Pytest",
        "Framework :: Flake8",
        "Intended Audience :: Telecommunications Industry",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
)
