#!/bin/bash

# for python
kaitai-struct-compiler -t python --python-package kaitai *.ksy ; black .

# for lua
kaitai-struct-compiler -t lua *.ksy ; mv *.lua wireshark/
