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
from json import loads
# import numpy as np
from re import split, sub
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem


class Utility(object):
    """Utility keywords for Requests operations."""

    def __init__(self):
        self._builtin = BuiltIn()
        self._os = OperatingSystem()

    def get_json_file(self, path):
        """Returns [http://goo.gl/o0X6Pp|JSON] object from [http://goo.gl/o0X6Pp|JSON] file
        with all variables replaced.

        Arguments:
        - ``path``: The path to JSON file.

        Examples:

        _request.json_
        | [{
        |     "bad": ${false},
        |     "good": ${true},
        |     "key": 5.5,
        |     "key2": "value2"
        | }]

        | @{var} = | Get JSON File | request.json |
        | # [{'key2': 'value2', 'bad': False, 'good': True, 'key': Decimal('5.5')}] |
        """
        content = self._os.get_file(path)
        content = self._builtin.replace_variables(content)
        content = sub(r'(False|True)', lambda match: match.group(1).lower(), content)
        logger.debug(content)
        return self.json_loads(content)

    def json_loads(self, text):
        # pylint: disable=line-too-long
        """Returns [http://goo.gl/o0X6Pp|JSON] object from [http://goo.gl/o0X6Pp|JSON] string
        with object restoration support.

        Arguments:
        - ``text``: JSON string.

        Supported object restoration:
        | `py/dict`                    |
        | `py/tuple`                   |
        | `py/set`                     |
        | `py/collections.namedtuple`  |
        | `py/collections.OrderedDict` |

        Examples:
        | @{var} = | JSON Loads | [{"key":"value"}] |
        | @{var} = | JSON Loads | [{"py/dict":{"key":"value"}}] |
        | @{var} = | JSON Loads | [{"py/tuple":(1,2,3)}] |
        | @{var} = | JSON Loads | [{"py/set":[1,2,3]}] |
        | @{var} = | JSON Loads | [{"py/collections.namedtuple":{"fields":"a b c","type":"NAME","values":(0,1,2)}}] |
        | @{var} = | JSON Loads | [{"py/collections.OrderedDict":[("key2",2),("key1",1)]}] |
        """
        # pylint: disable=line-too-long
        return loads(text, object_hook=self._restore, parse_float=Decimal)

    def natural_sort_list_of_dictionaries(self, items, key):
        """Returns natural sorted list of dictionaries.

        Arguments:
        - ``items``: List of dictionaries to be sorted.
        - ``key``: The dictionary key to be used to sort.

        Examples:
        | @{var} = | Natural Sort List Of Dictionaries | ${list} | key |
        """
        def _natural_sorter(item):
            """Returns splitted aphanumeric value list of given dictionary key."""
            return [self._cast_alphanumeric(text) for text in split('([0-9]+)', item[key])]
        return sorted(items, key=_natural_sorter)

    @staticmethod
    def _cast_alphanumeric(text):
        """Casts alphanumeric value."""
        return int(text) if text.isdigit() else text.lower()

    @staticmethod
    def _restore(dct):
        """Returns restored object."""
        if "py/dict" in dct:
            return dict(dct["py/dict"])
        if "py/tuple" in dct:
            return tuple(dct["py/tuple"])
        if "py/set" in dct:
            return set(dct["py/set"])
        if "py/collections.namedtuple" in dct:
            data = dct["py/collections.namedtuple"]
            return namedtuple(data["type"], data["fields"])(*data["values"])
        # if "py/numpy.ndarray" in dct:
        #     data = dct["py/numpy.ndarray"]
        #     return np.array(data["values"], dtype=data["dtype"])
        if "py/collections.OrderedDict" in dct:
            return OrderedDict(dct["py/collections.OrderedDict"])
        return dct
