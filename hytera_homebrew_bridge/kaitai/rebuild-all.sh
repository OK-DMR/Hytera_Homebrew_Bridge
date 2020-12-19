#!/bin/bash

# for python
kaitai-struct-compiler -t python --python-package hytera_homebrew_bridge.kaitai *.ksy ; black .

# for lua
kaitai-struct-compiler -t lua *.ksy ; mv *.lua wireshark/
