# compiling

https://doc.kaitai.io/ksy_reference.html

## dependencies

apt repository
```apt
deb https://dl.bintray.com/kaitai-io/debian_unstable jessie main
```
install compiler
```bash
apt install kaitai-struct-compiler
apt purge python3-kaitaistruct
```

from root of project install kaitai python environment, apt provided is old
```bash
pip3 install -r requirements.txt --user
```

## re-compiling
from this folder
```bash
kaitai-struct-compiler -t python --python-package kaitai *.ksy
# this is for unified formatting of generated sources, if this command fails for you, skip it
black .
```

