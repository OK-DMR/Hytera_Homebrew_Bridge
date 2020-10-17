--
-- String decoder functions
--

local lunicode = require(".unicode")

local stringdecode = {}

function stringdecode.decode(str, encoding)
    local enc = encoding and encoding:lower() or "ascii"

    if enc == "ascii" then
        return str
    elseif enc == "utf-8" then
	return lunicode.transcode(str, lunicode.utf8_dec, lunicode.utf8_enc, false, false)
    elseif enc == "sjis" then
	return table.concat(lunicode.decode(str, lunicode.sjis_dec, true))
    elseif enc == "cp437" then
        return lunicode.transcode(str, lunicode.cp437_dec, lunicode.utf8_enc, false, false)
    else
        error("Encoding " .. encoding .. " not supported")
    end
end

return stringdecode
