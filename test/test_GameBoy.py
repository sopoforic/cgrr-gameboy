# Classic Game Resource Reader (CGRR): Parse resources from classic games.
# Copyright (C) 2015  Tracy Poff
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
import os
import unittest

class Test_game_boy_a(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from yapsy.PluginManager import PluginManager

        manager = PluginManager()
        manager.setPluginPlaces(["formats"])
        manager.collectPlugins()
        cls.plugin = manager.getPluginByName("Game Boy Header").plugin_object

    def test_roundtrip(self):
        mock = (b'\x00\xC3\x50\x01\x48\x65\x72\x65\x20\x77\x6F\x75\x6C\x64\x20'
                b'\x75\x73\x75\x61\x6C\x6C\x79\x20\x62\x65\x20\x74\x68\x65\x20'
                b'\x4E\x69\x6E\x74\x65\x6E\x64\x6F\x20\x6C\x6F\x67\x6F\x2E\x20'
                b'\x44\x65\x6C\x65\x74\x65\x21\x54\x45\x53\x54\x20\x52\x4F\x4D'
                b'\x20\x54\x49\x54\x4C\x45\x00\x00\x54\x50\x00\x00\x03\x00\x01'
                b'\x33\x00\x1C\x43\x53')
        header = self.plugin.parse_header(mock)
        generated = self.plugin.generate_header(header)
        self.assertEqual(generated, mock)
