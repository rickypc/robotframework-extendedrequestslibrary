#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Richard Huang <rickypc@users.noreply.github.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import requests
import RequestsLibrary
from ExtendedSelenium2Library.version import get_version
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from robot import utils
requests.packages.urllib3.disable_warnings()
logging.getLogger('requests').setLevel(logging.WARNING)

__version__ = get_version()


class ExtendedRequestsLibrary(RequestsLibrary.RequestsLibrary):
    """ ExtendedRequestsLibrary is a HTTP client keyword library that uses
    the requests module from Kenneth Reitz https://github.com/kennethreitz/requests
    """

    def create_oauth2_session_with_client_credentials_grant(self, alias, token_url, tenant_id, tenant_secret,
                                                            base_url=None, headers={}, cookies=None, timeout=None,
                                                            proxies=None, verify=False):
        """Create and return an OAuth2 session to a server with client credentials grant access token.

        `alias` is a Robot Framework alias to identify the OAuth2 session

        `token_url` is url of the OAuth2 token server

        `tenant_id` is the client id obtained during registration with OAuth2 provider

        `tenant_secret` is the client secret obtained during registration with OAuth2 provider

        `base_url` is base url of the server

        `headers` is a Dictionary of default headers

        `cookies` is a Dictionary of default cookies

        `timeout` is the connection timeout

        `proxies` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        `verify` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create OAuth2 Session With Client Credentials Grant | Google | https://www.google.com | id | secret |
        """
        logger.debug('Creating OAuth2 Session With Client Credentials Grant using : alias=%s, token_url=%s, tenant_id=%s, ' +
                     'tenant_secret=%s, base_url=%s, headers=%s, cookies=%s, timeout=%s, proxies=%s, verify=%s ' %
                     (alias, token_url, tenant_id, tenant_secret, base_url, headers, cookies, timeout, proxies, verify))
        session = OAuth2Session(client=BackendApplicationClient(''))
        # cant use hooks :(
        session.url = base_url
        session.headers.update(headers)
        session.proxies = proxies if proxies else session.proxies
        session.verify = self.builtin.convert_to_boolean(verify)
        # cant pass these into the Session anymore
        self.timeout = timeout
        self.cookies = cookies
        self.verify = verify
        session.fetch_token(token_url, auth=HTTPBasicAuth(tenant_id, tenant_secret), verify=verify)
        self._cache.register(session, alias=alias)
        return session

    def create_oauth2_session_with_password_credentials_grant(self, alias, token_url, tenant_id, tenant_secret, username,
                                                              password, base_url=None, headers={}, cookies=None,
                                                              timeout=None, proxies=None, verify=False):
        """Create and return an OAuth2 session to a server with client credentials grant access token.

        `alias` is a Robot Framework alias to identify the OAuth2 session

        `token_url` is url of the OAuth2 token server

        `tenant_id` is the client id obtained during registration with OAuth2 provider

        `tenant_secret` is the client secret obtained during registration with OAuth2 provider

        `username` is the resource owner username

        `password` is the resource owner password

        `base_url` is base url of the server

        `headers` is a Dictionary of default headers

        `cookies` is a Dictionary of default cookies

        `timeout` is the connection timeout

        `proxies` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        `verify` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create OAuth2 Session With Password Credentials Grant | Google | https://www.google.com | id | secret | username | password |
        """
        logger.debug('Creating OAuth2 Session With Password Credentials Grant using : alias=%s, token_url=%s, ' +
                     'tenant_id=%s, tenant_secret=%s, username=%s, password=%s, base_url=%s, headers=%s, cookies=%s, ' +
                     'timeout=%s, proxies=%s, verify=%s ' % (alias, token_url, tenant_id, tenant_secret, username,
                                                             password, base_url, headers, cookies, timeout, proxies,
                                                             verify))
        session = OAuth2Session(client=LegacyApplicationClient(''))
        # cant use hooks :(
        session.url = base_url
        session.headers.update(headers)
        session.proxies = proxies if proxies else session.proxies
        session.verify = self.builtin.convert_to_boolean(verify)
        # cant pass these into the Session anymore
        self.timeout = timeout
        self.cookies = cookies
        self.verify = verify
        session.fetch_token(token_url, auth=HTTPBasicAuth(tenant_id, tenant_secret), username=username,
                            password=password, verify=verify)
        self._cache.register(session, alias=alias)
        return session