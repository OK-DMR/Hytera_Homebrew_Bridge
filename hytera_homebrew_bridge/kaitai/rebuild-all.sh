#!/bin/bash

# for python
kaitai-struct-compiler -t python --python-package hytera_homebrew_bridge.kaitai *.ksy ; black .
