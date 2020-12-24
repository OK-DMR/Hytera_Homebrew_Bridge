# Hytera Homebrew Bridge

![.github/workflows/sanity.yml](https://github.com/smarek/Hytera_Homebrew_Bridge/workflows/Sanity/badge.svg?branch=master)
![Code Style: Python Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/github/license/smarek/Hytera_Homebrew_Bridge)


**21.12.2020: We've entered alpha testing phase, see instructions below, on how to install and test**

----

This software will interconnect your Hytera repeater (tested RD625 and RD985) with MMDVM server (HBlink, DMRGateway, ...)  
It does not require running under root/admin user, if you bind to ports over 1024

----
## Simple install:
```shell
# You need to have Python3 installed, at least version 3.7
$ python3 -m pip install pip wheel setuptools --upgrade
$ python3 -m pip install hytera-homebrew-bridge --upgrade
# download config file
$ curl "https://raw.githubusercontent.com/OK-DMR/Hytera_Homebrew_Bridge/master/settings.ini.minimal.default" -o settings.ini
# Now edit settings.ini
# Hytera: You must provide at least IPSC IP + ports (P2P, DMR and RDAC)
# MMDVM: You must provide at least local_ip, master_ip, port and password
# See "settings.ini.minimal.default" for required params / minimal configuration
$ hytera-homebrew-bridge.py settings.ini
```

----
## Install on Windows 

To get software running on Windows, you need to install appropriate Python 3.7+ package (depending on your Windows version),
and you need to install dependencies (MSVC++ 14) required to build **bitarray** dependency

- Microsoft Visual C++ Build Tools v14.0
  - Use [visualcppbuildtools_full.exe](https://go.microsoft.com/fwlink/?LinkId=691126) and install with default configuration
  
Then you should be able to use **Simple install**
```shell
# From standard Windows Command Line (cmd.exe) 
$ python -m pip install pip wheel setuptools --upgrade
$ python -m pip install hytera-homebrew-bridge --upgrade
# Download settings from the project, settings.ini.minimal.default or settings.ini.default and modify it
$ 
```


----
## Developer install:

Run the software without installing to Python packages, so you can edit code and run the edits

```shell
# Optionally uninstall the version installed in system
# python3
$ git clone https://github.com/OK-DMR/Hytera_Homebrew_Bridge.git
$ cd Hytera_Homebrew_Bridge
# You can use either settings.ini.default (all configuration params) or settings.ini.minimal.default (only required params)
$ cp settings.ini.default settings.ini
$ apt-get install libsnmp-dev snmp-mibs-downloader gcc python-dev
$ python3 -m pip install -r requirements.txt --user --upgrade
# Dependencies to run tests (pytest, pcapng parsing, ...)
$ python3 -m pip install -r requirements.development.txt --user --upgrade
$ python3 bin/hytera-homebrew-bridge.py settings.ini
```

----

Project is licensed under AGPLv3 and uses parts of other software, mentioned in NOTICE

----

This project is intended for educational/scientific purposes, and for HAM community to use non-commercialy.  
Use at your own risk, and expect no warranties.
