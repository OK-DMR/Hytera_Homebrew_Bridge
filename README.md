# Hytera Homebrew Bridge

![.github/workflows/sanity.yml](https://github.com/smarek/Hytera_Homebrew_Bridge/workflows/Sanity/badge.svg?branch=master)
![Code Style: Python Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/github/license/smarek/Hytera_Homebrew_Bridge)


**21.12.2020: We've entered alpha testing phase, see instructions below, on how to install and test**

----

This software will interconnect your Hytera repeater (tested RD625 and RD985) with MMDVM server (HBlink, DMRGateway, ...)

----
## Simple install:
```shell
$ python3 -m pip install hytera-homebrew-bridge
$ curl "https://raw.githubusercontent.com/OK-DMR/Hytera_Homebrew_Bridge/master/settings.ini.default" -o settings.ini
# Now edit settings.ini
# Hytera: You must provide at least IPSC IP + ports (P2P, DMR and RDAC)
# MMDVM: You must provide at least local_ip, master_ip, port and password
$ hytera-homebrew-bridge.py settings.ini
```

----
## Developer install:

```shell
$ git clone https://github.com/OK-DMR/Hytera_Homebrew_Bridge.git
$ cd Hytera_Homebrew_Bridge
$ cp settings.ini.default settings.ini
$ apt-get install libsnmp-dev snmp-mibs-downloader gcc python-dev
$ pip3 install -r requirements.txt --user --upgrade
$ pip3 install -r requirements.development.txt --user --upgrade
$ python3 bin/hytera-homebrew-bridge.py settings.ini
```

----

Project is licensed under AGPLv3 and uses parts of other software, mentioned in NOTICE

----

This project is intended for educational/scientific purposes, and for HAM community to use non-commercialy.  
Use at your own risk, and expect no warranties.
