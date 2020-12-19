from setuptools import setup

setup(
    name="hytera-homebrew-bridge",
    description="Connect Hytera IPSC repeater to MMDVM system such as HBlink, DMRGateway",
    url="https://github.com/OK-DMR/Hytera_Homebrew_Bridge",
    author="Marek Sebera",
    author_email="marek.sebera@gmail.com",
    license="AGPL-3.0",
    version="2020.1",
    packages=[
        "hytera_homebrew_bridge",
        "hytera_homebrew_bridge.kaitai",
        "hytera_homebrew_bridge.lib",
        "hytera_homebrew_bridge.tests",
    ],
    zip_safe=False,
    scripts=["bin/hytera-homebrew-bridge.py"],
    keywords="mmdvm dmr hytera repeater",
)
