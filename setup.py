#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Extended Requests Library - a HTTP client library with OAuth2 support.
#    Copyright (C) 2015  Richard Huang <rickypc@users.noreply.github.com>
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

# To use a consistent encoding
import codecs
from os.path import abspath, dirname, join
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

LIBRARY_NAME = 'ExtendedRequestsLibrary'
CWD = abspath(dirname(__file__))
execfile(join(CWD, 'src', LIBRARY_NAME, 'version.py'))

with codecs.open(join(CWD, 'README.rst'), encoding='utf-8') as reader:
    LONG_DESCRIPTION = reader.read()

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version=VERSION, # pylint: disable=undefined-variable
    description='Extended HTTP client library for Robot Framework with OAuth2 support',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/rickypc/robotframework-%s' % LIBRARY_NAME.lower(),
    author='Richard Huang',
    author_email='rickypc@users.noreply.github.com',
    license='AGPL 3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='robot framework extended testing automation requests oauth2 oauth rest api',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['robotframework', 'robotframework-requests', 'requests-oauthlib']
)
