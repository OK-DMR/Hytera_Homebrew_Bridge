# runtime-only no dissector yet

This folder contains modified Lua kaitai-struct-compiler results, with modified runtime from github.com/kaitai-io/kaitai_struct_lua_runtime

Install the runtime to wireshark using `mkdir -p ~/.local/lib/wireshark/plugins ; cp *.lua ~/.local/lib/wireshark/plugins`

Baking the new .lua from .ksy will require you to modify the results, if there are any bitwise operations
```


```
