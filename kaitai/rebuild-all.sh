#!/bin/bash

kaitai-struct-compiler -t python --python-package kaitai *.ksy ; black .
