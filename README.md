# Hytera Homebrew Bridge (HHB)

[![.github/workflows/sanity.yml](https://img.shields.io/github/actions/workflow/status/OK-DMR/Hytera_Homebrew_Bridge/sanity.yml?style=flat-square&branch=master)](https://github.com/OK-DMR/Hytera_Homebrew_Bridge/actions)
[![Code Style: Python Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/OK-DMR/Hytera_Homebrew_Bridge?style=flat-square)](https://github.com/OK-DMR/Hytera_Homebrew_Bridge/blob/master/LICENSE)
[![Last released version](https://img.shields.io/pypi/v/hytera-homebrew-bridge?style=flat-square)](https://pypi.org/project/hytera-homebrew-bridge/)
[![PyPI downloads](https://img.shields.io/pypi/dd/hytera-homebrew-bridge?style=flat-square)](https://libraries.io/pypi/hytera-homebrew-bridge)
[![Python versions](https://img.shields.io/pypi/pyversions/hytera-homebrew-bridge?style=flat-square)](https://pypi.org/project/hytera-homebrew-bridge/)
[![Wheel](https://img.shields.io/pypi/wheel/hytera-homebrew-bridge?style=flat-square)](https://pypi.org/project/hytera-homebrew-bridge/#files)
[![Codecov](https://img.shields.io/codecov/c/github/OK-DMR/Hytera_Homebrew_Bridge?style=flat-square)](https://app.codecov.io/gh/OK-DMR/Hytera_Homebrew_Bridge)

----

This software will interconnect your Hytera repeater with MMDVM server (such as hblink, dmrgateway, etc...)

----
## Install:
```shell
# upgrade important system dependencies, "wheel" is essential
$ python3 -m pip install pip wheel setuptools --upgrade
# install (and upgrade) hytera-homebrew-bridge
$ python3 -m pip install hytera-homebrew-bridge --upgrade
$ hytera-homebrew-bridge <path to settings.ini> <optionally path to logging.ini>
```


----
## Develop:

```shell
# clone repo
$ git clone https://github.com/OK-DMR/Hytera_Homebrew_Bridge.git
# change path into cloned repo
$ cd Hytera_Homebrew_Bridge
# You can use either settings.ini.default (all configuration params) or settings.ini.minimal.default (only required params)
$ cp settings.ini.default settings.ini
# install current directory to local site-packages in editable mode
$ python3 -m pip install -e .
# run hytera-homebrew-bridge with params
$ hytera-homebrew-bridge <path to settings.ini> <optionally path to logging.ini>
```

----
## FAQ

- Q: Difference between SNMP family/community 'public' and 'hytera'?
  - A: Some repeaters have non-changeable SNMP setting, and it appears it is usually either 'public' or 'hytera', if SNMP does not work for you, try changing the value to the other one
- Q: RDAC identification restarts unexpectedly or does not work at all, what can I try to fix it?
  - A: Check the programming in CPS, there might be multiple incorrect settings
    1. Open `Conventional > Channel > Digital Channel (or analog) > Digital IP Multi-Site Connect (4th from top in channel detail) must be set to "Slot 1 & Slot 2"`
    2. Open `Conventional > General Settings > Access Manager` and in the section "Multisite Access Management" either disable the management or set correct list
- Q: SNMP does not work correctly, what can I try to fix it?
  - A: Check if SNMP port is set to 161 in `Conventional > General Settings > Network` section `SNMP` at the bottom
- Q: I'm not getting the upstream connection and/or I'm seeing a lot of logs similar to "MMDVMProtocol - Sending Login Request"
  - A: This is usually misconfiguration of Hytera repeater, if you do not see any logs with 'RDAC' or the long packet with 'REPEATER SNMP CONFIGURATION' info. In such cases you should check if the Hytera repeater is programmed correctly as slave and the IP/ports do match the HHB startup log saying 'Hytera Repeater is expected to connect at xxx.xxx.xxx.xxx'

----

Project is licensed under AGPLv3 and uses parts of other software, mentioned in NOTICE

----

This project is intended for educational/scientific purposes, and for HAM community to use non-commercialy.  
Use at your own risk, and expect no warranties.
