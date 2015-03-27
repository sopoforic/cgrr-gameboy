# Classic Game Resource Reader (CGRR): Parse resources from classic games.
# Copyright (C) 2014  Tracy Poff
#
# This file is part of CGRR.
#
# CGRR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CGRR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CGRR.  If not, see <http://www.gnu.org/licenses/>.
"""Parses GameBoy ROM headers."""
import os
from collections import namedtuple
from enum import Enum

import yapsy

import utilities
from errors import UnsupportedSoftwareException
from utilities import File, FileReader

class GameBoy(yapsy.IPlugin.IPlugin):
    """Parses GameBoy ROM headers."""

    key = "game_boy_a"
    title = "GameBoy Header"
    developer = "Nintendo"
    description = "GameBoy Header"

    class RomSize(Enum):
        ROM_256kbit  = 0
        ROM_512kbit  = 1
        ROM_1024kbit = 2
        ROM_2048kbit = 3
        ROM_4096kbit = 4

    class RamSize(Enum):
        RAM_None    = 0
        RAM_16kbit  = 1
        RAM_64kbit  = 2
        RAM_256kbit = 3

    class DestinationCode(Enum):
        JAPAN     = 0
        NOT_JAPAN = 1

    gb_header_reader = FileReader(
        format = [
            ("begin", "4s"), # usually \x00\xC3\x50\x01
            ("nintendo_logo", "48s"), # must match or GB stops execution
            ("title", "16s"), # upper-case ASCII, 0 padded
            ("licensee", "2s"),
            ("sgb_flag", "B"), # \x00 = no SGB support, \x03 = SGB support
            ("cartridge_type", "B"),
            ("rom_size", "B"),
            ("ram_size", "B"),
            ("destination_code", "B"), # \x00 = Japan, \x01 = not Japan
            ("old_licensee", "B"), # if \x33, see licensee
            ("mask_rom_version", "B"), # usually \x00
            ("header_checksum", "B"),
            ("global_checksum", "H"),
        ],
        massage_in = {
            "title" : (lambda s: s.decode('ascii').rstrip('\x00')),
            "rom_size" : (lambda b: GameBoy.RomSize(b)),
            "ram_size" : (lambda b: GameBoy.RamSize(b)),
            "destination_code" : (lambda b: GameBoy.DestinationCode(b)),
        },
        massage_out = {
            "title" : (lambda s: s[:16].upper().ljust(16, '\x00').encode('ascii')),
            "rom_size" : (lambda b: b.value),
            "ram_size" : (lambda b: b.value),
            "destination_code" : (lambda b: b.value),
        },
        byte_order = "<"
    )

    @staticmethod
    def read_header(path):
        """Read a GameBoy ROM header."""
        header_size = GameBoy.gb_header_reader.struct.size
        with open(path, "rb") as rom:
            rom.seek(0x100)
            return GameBoy.gb_header_reader.unpack(rom.read(header_size))
