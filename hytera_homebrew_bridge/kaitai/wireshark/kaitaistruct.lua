local class = require("class")
local stringstream = require("string_stream")
local lunpack = require("struct").unpack

local function try_require(name)
    local success, mod = pcall(require, name)
    if success then
        return mod
    else
        return nil
    end
end

-- bit is required in translated lua files, so provide it in this parent module
bit = try_require('bit') or try_require('bit32') or error[[no bitwise library found]]

KaitaiStruct = class.class()

function KaitaiStruct:_init(io)
    self._io = io
end

function KaitaiStruct:close()
    self._io:close()
end

function KaitaiStruct:from_file(filename)
    local inp = assert(io.open(filename, "rb"))

    return self(KaitaiStream(inp))
end

function KaitaiStruct:from_string(s)
    local ss = stringstream(s)

    return self(KaitaiStream(ss))
end

KaitaiStream = class.class()

function KaitaiStream:_init(io)
    self._io = io
    self:align_to_byte()
end

function KaitaiStream:close()
    self._io:close()
end

--=============================================================================
-- Stream positioning
--=============================================================================

function KaitaiStream:is_eof()
    if self.bits_left > 0 then
        return false
    end
    local current = self._io:seek()
    local dummy = self._io:read(1)
    self._io:seek("set", current)

    return dummy == nil
end

function KaitaiStream:seek(n)
    self._io:seek("set", n)
end

function KaitaiStream:pos()
    return self._io:seek()
end

function KaitaiStream:size()
    local current = self._io:seek()
    local size = self._io:seek("end")
    self._io:seek("set", current)

    return size
end

--=============================================================================
-- Integer numbers
--=============================================================================

-------------------------------------------------------------------------------
-- Signed
-------------------------------------------------------------------------------

function KaitaiStream:read_s1()
    return lunpack('b', self._io:read(1))
end

--.............................................................................
-- Big-endian
--.............................................................................

function KaitaiStream:read_s2be()
    return lunpack('>h', self._io:read(2))
end

function KaitaiStream:read_s4be()
    return lunpack('>i', self._io:read(4))
end

function KaitaiStream:read_s8be()
    return lunpack('>l', self._io:read(8))
end

--.............................................................................
-- Little-endian
--.............................................................................

function KaitaiStream:read_s2le()
    return lunpack('<h', self._io:read(2))
end

function KaitaiStream:read_s4le()
    return lunpack('<i', self._io:read(4))
end

function KaitaiStream:read_s8le()
    return lunpack('<l', self._io:read(8))
end

-------------------------------------------------------------------------------
-- Unsigned
-------------------------------------------------------------------------------

function KaitaiStream:read_u1()
    return lunpack('B', self._io:read(1))
end

--.............................................................................
-- Big-endian
--.............................................................................

function KaitaiStream:read_u2be()
    return lunpack('>H', self._io:read(2))
end

function KaitaiStream:read_u4be()
    return lunpack('>I', self._io:read(4))
end

function KaitaiStream:read_u8be()
    return lunpack('>L', self._io:read(8))
end

--.............................................................................
-- Little-endian
--.............................................................................

function KaitaiStream:read_u2le()
    return lunpack('<H', self._io:read(2))
end

function KaitaiStream:read_u4le()
    return lunpack('<I', self._io:read(4))
end

function KaitaiStream:read_u8le()
    return lunpack('<L', self._io:read(8))
end

--=============================================================================
-- Floating point numbers
--=============================================================================

-------------------------------------------------------------------------------
-- Big-endian
-------------------------------------------------------------------------------

function KaitaiStream:read_f4be()
    return lunpack('>f', self._io:read(4))
end

function KaitaiStream:read_f8be()
    return lunpack('>d', self._io:read(8))
end

-------------------------------------------------------------------------------
-- Little-endian
-------------------------------------------------------------------------------

function KaitaiStream:read_f4le()
    return lunpack('<f', self._io:read(4))
end

function KaitaiStream:read_f8le()
    return lunpack('<d', self._io:read(8))
end

--=============================================================================
-- Unaligned bit values
--=============================================================================

function KaitaiStream:align_to_byte()
    self.bits = 0
    self.bits_left = 0
end

function KaitaiStream:read_bits_int_be(n)
    local bits_needed = n - self.bits_left
    if bits_needed > 0 then
        -- 1 bit  => 1 byte
        -- 8 bits => 1 byte
        -- 9 bits => 2 bytes
        local bytes_needed = math.ceil(bits_needed / 8)
        local buf = self._io:read(bytes_needed)
        for i = 1, #buf do
            local byte = buf:byte(i)
            self.bits = bit.lshift(self.bits, 8)
            self.bits = bit.bor(self.bits, byte)
            self.bits_left = self.bits_left + 8
        end
    end

    -- Raw mask with required number of 1s, starting from lowest bit
    local mask = bit.lshift(1, n) - 1
    -- Shift self.bits to align the highest bits with the mask & derive reading result
    local shift_bits = self.bits_left - n
    local res = bit.band(bit.rshift(self.bits, shift_bits), mask)
    -- Clear top bits that we've just read => AND with 1s
    self.bits_left = self.bits_left - n
    mask = bit.lshift(1, self.bits_left) - 1
    self.bits = bit.band(self.bits, mask)

    return res
end

--
-- Unused since Kaitai Struct Compiler v0.9+ - compatibility with older versions
--
-- Deprecated, use read_bits_int_be() instead.
--
function KaitaiStream:read_bits_int(n)
    return self:read_bits_int_be(n)
end

function KaitaiStream:read_bits_int_le(n)
    local bits_needed = n - self.bits_left
    if bits_needed > 0 then
        -- 1 bit  => 1 byte
        -- 8 bits => 1 byte
        -- 9 bits => 2 bytes
        local bytes_needed = math.ceil(bits_needed / 8)
        local buf = self._io:read(bytes_needed)
        for i = 1, #buf do
            local byte = buf:byte(i)
            self.bits = bit.lshift(self.bits, 8)
            self.bits = bit.bor(self.bits, byte)
            self.bits_left = self.bits_left + 8
        end
    end

    -- Raw mask with required number of 1s, starting from lowest bit
    local mask = bit.lshift(1, n) - 1
    -- Shift mask to align with highest bits available in self.bits
    local shift_bits = self.bits_left - n
    mask = bit.lshift(mask, shift_bits)
    -- Derive reading result
    local res = bit.rshift(bit.band(self.bits, mask), shift_bits)
    -- Clear top bits that we've just read => AND with 1s
    self.bits_left = self.bits_left - n
    mask = bit.lshift(1, self.bits_left) - 1
    self.bits = bit.band(self.bits, mask)

    return res
end

--=============================================================================
-- Byte arrays
--=============================================================================

function KaitaiStream:read_bytes(n)
    local r = self._io:read(n)
    if r == nil then
        r = ""
    end

    if r:len() < n then
        error("requested " .. n .. " bytes, but got only " .. r:len() .. " bytes")
    end

    return r
end

function KaitaiStream:read_bytes_full()
    local r = self._io:read("*all")
    if r == nil then
        r = ""
    end

    return r
end

function KaitaiStream:read_bytes_term(term, include_term, consume_term, eos_error)
    local r = ""

    while true do
        local c = self._io:read(1)

        if c == nil then
            if eos_error then
                error("end of stream reached, but no terminator " .. term .. " found")
            else
                return r
            end
        elseif c:byte() == term then
            if include_term then
                r = r .. c
            end

            if not consume_term then
                local current = self._io:seek()
                self._io:seek("set", current - 1)
            end

            return r
        else
            r = r .. c
        end
    end
end

function KaitaiStream:ensure_fixed_contents(expected)
    local actual = self:read_bytes(#expected)

    if actual ~= expected then
        error("unexpected fixed contents: got " ..  actual .. ", was waiting for " .. expected)
    end

    return actual
end

function KaitaiStream.bytes_strip_right(src, pad_byte)
    local new_len = src:len()

    while new_len >= 1 and src:byte(new_len) == pad_byte do
        new_len = new_len - 1
    end

    return src:sub(1, new_len)
end

function KaitaiStream.bytes_terminate(src, term, include_term)
    local new_len = 1
    local max_len = src:len()

    while new_len <= max_len and src:byte(new_len) ~= term do
        new_len = new_len + 1
    end

    if include_term and new_len <= max_len then
        new_len = new_len + 1
    end

    return src:sub(1, new_len - 1)
end

--=============================================================================
-- Byte array processing
--=============================================================================

function KaitaiStream.process_xor_one(data, key)
    local r = ""

    for i = 1, #data do
        local c = bit.bxor(data:byte(i), key)
        r = r .. string.char(c)
    end

    return r
end

function KaitaiStream.process_xor_many(data, key)
    local r = ""
    local kl = key:len()
    local ki = 1

    for i = 1, #data do
        local c = bit.bxor(data:byte(i), key:byte(ki))
        r = r .. string.char(c)
        ki = ki + 1
        if ki > kl then
            ki = 1
        end
    end

    return r
end

function KaitaiStream.process_rotate_left(data, amount, group_size)
    if group_size ~= 1 then
        error("unable to rotate group of " .. group_size .. " bytes yet")
    end

    local result = ""
    local mask = group_size * 8 - 1
    local anti_amount = bit.band(-amount, mask)

    for i = 1, #data  do
        local c = data:byte(i)
        c = bit.bor(bit.band(bit.lshift(c, amount), 0xFF), bit.rshift(c, anti_amount))
        result = result .. string.char(c)
    end

    return result
end
