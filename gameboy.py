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

from cgrr import File, FileReader

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
    ROM_13       = 13  # 4 in 1 (Europe) (Sachen)
    ROM_255      = 255 # Pro Action Replay (Europe)

class RamSize(Enum):
    RAM_None    = 0
    RAM_2kbyte  = 1
    RAM_8kbyte  = 2
    RAM_32kbyte = 3
    RAM_4       = 4   # Game Boy Camera
    RAM_56      = 56  # Beast Fighter (Taiwan) (Sachen)
    RAM_255     = 255 # Pro Action Replay (Europe)

class DestinationCode(Enum):
    JAPAN     = 0
    NOT_JAPAN = 1
    # some unlicensed games use different codes
    DEST_53   = 53  # Beast Fighter (Taiwan) (Sachen)
    DEST_137  = 137 # 4 in 1 (Europe) (Sachen)
    DEST_255  = 255 # Pro Action Replay (Europe)

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
        # I'm using cp437 rather than ascii here because one game,
        # Gluecksrad, actually uses that encoding, and it neatly handles
        # the few GB games with a 0x80 at offset 0x143. It conveniently also
        # works on Sachen's 4-in-1 games, which have a nonstandard format.
        "title" : (lambda s: s.decode('cp437').rstrip('\x00')),
        "rom_size" : (lambda b: RomSize(b)),
        "ram_size" : (lambda b: RamSize(b)),
        "destination_code" : (lambda b: DestinationCode(b)),
    },
    massage_out = {
        "title" : (lambda s: s[:16].upper().ljust(16, '\x00').encode('cp437')),
        "rom_size" : (lambda b: b.value),
        "ram_size" : (lambda b: b.value),
        "destination_code" : (lambda b: b.value),
    },
    byte_order = "<"
)

HEADER_SIZE = gb_header_reader.struct.size

def identify(path):
    """Verify that the file given in path is a supported ROM."""
    calculated_checksum = 0
    actual_checksum = None
    with open(path, "rb") as rom:
        rom.seek(0x134)
        data = rom.read(25)
        calculated_checksum = (calculated_checksum - sum(data) - 25) & 255
        actual_checksum = rom.read(1)[0]
    if calculated_checksum != actual_checksum:
        False
    return True # TODO: return the decoder instead? return the decoded rom?

def calculate_header_checksum(header):
    data = generate_header(header)
    checksum = (0 - sum([data[i] for i in range(0x34, 0x4d)]) - 25) & 255
    return checksum

def parse_header(data):
    if len(data) != HEADER_SIZE:
        raise ValueError("Wrong header size!")
    return gb_header_reader.unpack(data)

def generate_header(header):
    return gb_header_reader.pack(header)

def read_header(path):
    """Read a Game Boy ROM header."""
    with open(path, "rb") as rom:
        rom.seek(0x100)
        return parse_header(rom.read(HEADER_SIZE))
