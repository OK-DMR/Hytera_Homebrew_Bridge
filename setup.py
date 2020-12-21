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
    install_requires=[
        "configparser>=5.0.0",
        "kaitaistruct>=0.9",
        "easysnmp>=0.2.5",
        "asyncio>=3.4.3",
        "dmr_utils3>=0.1.29",
        "bitarray>=1.6.1",
    ],
)
