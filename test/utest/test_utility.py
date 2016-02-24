#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Extended Requests Library - a HTTP client library with OAuth2 support.
#    Copyright (c) 2015, 2016 Richard Huang <rickypc@users.noreply.github.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Extended Requests Library - a HTTP client library with OAuth2 support.
"""

from collections import namedtuple, OrderedDict
from decimal import Decimal
from sys import path
path.append('src')
from ExtendedRequestsLibrary.keywords import Utility
from os.path import dirname
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
import mock
import unittest


class UtilityTests(unittest.TestCase):
    """Utility keyword test class."""

    def setUp(self):
        """Instantiate the utility class."""
        self.utility = Utility()

    def test_class_should_initiate(self):
        """Class init should instantiate required classes."""
        self.assertIsInstance(self.utility._builtin, BuiltIn)
        self.assertIsInstance(self.utility._os, OperatingSystem)

    def test_should_return_json(self):
        """De-serialize JSON file to JSON object correctly."""
        expected = [{'bad': False, 'good': True, 'key': Decimal(5.5), 'key2': 'value2'}]

        def side_effect(text):
            return text.replace('${false}', 'False').replace('${true}', 'True')
        self.utility._builtin.replace_variables = mock.MagicMock(side_effect=side_effect)
        self.assertEqual(self.utility.get_json_file('%s/requests.json' % dirname(__file__)),
                         expected)

    def test_json_should_loads(self):
        """De-serialize JSON string to JSON object correctly."""
        actual = '[{"key": 5.5, "key2": "value2"}]'
        expected = [{'key': Decimal(5.5), 'key2': 'value2'}]
        self.assertEqual(self.utility.json_loads(actual), expected)

    def test_object_restore_dict(self):
        """Should restore dict object successfully."""
        actual = {"py/dict": {"key": "value"}}
        expected = dict({"key": "value"})
        self.assertEqual(self.utility._restore(actual), expected)

    def test_object_restore_tuple(self):
        """Should restore tuple object successfully."""
        actual = {"py/tuple": (1, 2, 3)}
        expected = tuple((1, 2, 3))
        self.assertEqual(self.utility._restore(actual), expected)

    def test_object_restore_set(self):
        """Should restore set object successfully."""
        actual = {"py/set": [1, 2, 3]}
        expected = set([1, 2, 3])
        self.assertEqual(self.utility._restore(actual), expected)

    def test_object_restore_namedtuple(self):
        """Should restore namedtuple object successfully."""
        actual = {"py/collections.namedtuple":
                  {"type": "MINE", "fields": "a b c", "values": (0, 1, 2)}}
        expected = namedtuple('MINE', 'a b c')._make(range(3))
        self.assertEqual(self.utility._restore(actual), expected)

    def test_object_restore_OrderedDict(self):
        """Should restore OrderedDict object successfully."""
        actual = {"py/collections.OrderedDict": [('key2', 2), ('key1', 1)]}
        expected = OrderedDict([('key2', 2), ('key1', 1)])
        self.assertEqual(self.utility._restore(actual), expected)
