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
"""Parses Game Boy ROM headers."""
import os
from collections import namedtuple
from enum import Enum

import yapsy

import utilities
from errors import UnsupportedSoftwareException
from utilities import File, FileReader

class GameBoy(yapsy.IPlugin.IPlugin):
    """Parses Game Boy ROM headers."""

    key = "game_boy_a"
    title = "Game Boy Header"
    developer = "Nintendo"
    description = "Game Boy Header"

    class RomSize(Enum):
        ROM_32kbyte  = 0
        ROM_64kbyte  = 1
        ROM_128kbyte = 2
        ROM_256kbyte = 3
        ROM_512kbyte = 4
        ROM_1mbyte   = 5
        ROM_2mbyte   = 6
        ROM_4mbyte   = 7
        ROM_1_1mbyte = 0x52
        ROM_1_2mbyte = 0x53
        ROM_1_5mbyte = 0x54

    class RamSize(Enum):
        RAM_None    = 0
        RAM_2kbyte  = 1
        RAM_8kbyte  = 2
        RAM_32kbyte = 3

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
        """Read a Game Boy ROM header."""
        header_size = GameBoy.gb_header_reader.struct.size
        with open(path, "rb") as rom:
            rom.seek(0x100)
            return GameBoy.gb_header_reader.unpack(rom.read(header_size))
