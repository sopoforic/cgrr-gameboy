gameboy
=======

This module parses Game Boy ROM headers.

Usage
=====

To parse a ROM header:

```python
>>> import gameboy
>>> gameboy.read_header("Super Mario Land (World).gb")
{
  'begin': b'\x00\xc3P\x01',
  'nintendo_logo': ..., # removed for space
  'title': 'SUPER MARIOLAND',
  'licensee': b'\x00\x00',
  'sgb_flag': 0,
  'cartridge_type': 1,
  'rom_size': <RomSize.ROM_64kbyte: 1>,
  'ram_size': <RamSize.RAM_None: 0>,
  'destination_code': <DestinationCode.JAPAN: 0>
  'old_licensee': 1,
  'mask_rom_version': 0,
  'header_checksum': 158,
  'global_checksum': 27457,
}
```

This dictionary can be modified and re-encoded using `generate_header`

```python
import gameboy
header = gameboy.read_header("path/to/rom.gb")

header["title"] = "AWESOME HACK"

data = gameboy.generate_header(header)
```

The modified header can be re-inserted into a ROM file.

Requirements
============

* `pip install -r requirements.txt`
* If you're using python < 3.4, also do `pip install enum`

License
=======

This module is available under the GPL v3 or later. See the file COPYING for
details.

[![Build Status](https://travis-ci.org/sopoforic/cgrr-gameboy.svg?branch=master)](https://travis-ci.org/sopoforic/cgrr-gameboy)
