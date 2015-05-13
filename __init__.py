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
from ExtendedRequestsLibrary.version import get_version
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from robot.api import logger
from urlparse import urlparse
requests.packages.urllib3.disable_warnings()
logging.getLogger('requests').setLevel(logging.WARNING)

__version__ = get_version()


class ExtendedRequestsLibrary(RequestsLibrary.RequestsLibrary):
    """ ExtendedRequestsLibrary is a HTTP client keyword library that uses
    the requests module from Kenneth Reitz https://github.com/kennethreitz/requests
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        RequestsLibrary.RequestsLibrary.__init__(self)
        self._primers = {}

    def create_oauth2_session_with_client_credentials_grant(self, alias, token_url, tenant_id, tenant_secret,
                                                            base_url=None, headers={}, cookies=None, timeout=90,
                                                            proxies=None, verify=False, **kwargs):
        """Create and return an OAuth2 session to a server with client credentials grant access token.

        `alias` is a Robot Framework alias to identify the OAuth2 session

        `token_url` is url of the OAuth2 token server

        `tenant_id` is the client id obtained during registration with OAuth2 provider

        `tenant_secret` is the client secret obtained during registration with OAuth2 provider

        `base_url` is base url of the server

        `headers` is a Dictionary of default headers

        `cookies` is a Dictionary of default cookies

        `timeout` is the connection timeout in seconds

        `proxies` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        `verify` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create OAuth2 Session With Client Credentials Grant | Google | https://www.google.com | id | secret |
        """
        log_message = ('Creating OAuth2 Session With Client Credentials Grant using: alias=%s, token_url=%s, '
                       'tenant_id=%s, tenant_secret=%s, base_url=%s, headers=%s, cookies=%s, timeout=%s, proxies=%s, '
                       'verify=%s')
        logger.debug(log_message % (alias, token_url, tenant_id, tenant_secret, base_url, headers, cookies, timeout,
                                    proxies, verify))
        self._register_urls(base_url, token_url)
        session = OAuth2Session(client=BackendApplicationClient(''))
        self._session_init(session, base_url, headers, proxies, verify, timeout, cookies)
        session.fetch_token(token_url, auth=HTTPBasicAuth(tenant_id, tenant_secret), verify=verify, **kwargs)
        self._cache.register(session, alias=alias)
        return session

    def create_oauth2_session_with_password_credentials_grant(self, alias, token_url, tenant_id, tenant_secret, username,
                                                              password, base_url=None, headers={}, cookies=None,
                                                              timeout=90, proxies=None, verify=False, **kwargs):
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

        `timeout` is the connection timeout in seconds

        `proxies` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        `verify` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create OAuth2 Session With Password Credentials Grant | Google | https://www.google.com | id | secret | username | password |
        """
        log_message = ('Creating OAuth2 Session With Password Credentials Grant using: alias=%s, token_url=%s, '
                       'tenant_id=%s, tenant_secret=%s, username=%s, password=%s, base_url=%s, headers=%s, '
                       'cookies=%s, timeout=%s, proxies=%s, verify=%s')
        logger.debug(log_message % (alias, token_url, tenant_id, tenant_secret, username, password, base_url, headers,
                                    cookies, timeout, proxies, verify))
        self._register_urls(base_url, token_url)
        session = OAuth2Session(client=LegacyApplicationClient(''))
        self._session_init(session, base_url, headers, proxies, verify, timeout, cookies)
        session.fetch_token(token_url, auth=HTTPBasicAuth(tenant_id, tenant_secret), username=username,
                            password=password, verify=verify, **kwargs)
        self._cache.register(session, alias=alias)
        return session

    def delete_request(self, alias, uri, data=(), headers=None, allow_redirects=None, **kwargs):
        """Send a DELETE request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the DELETE request to

        `data` a dictionary of key-value pairs that will be urlencoded and sent as DELETE data or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.delete(self._get_url(session, uri), data=self._utf8_urlencode(data), headers=headers,
                                  cookies=self.cookies, timeout=self.timeout, allow_redirects=bool(allow_redirects),
                                  **kwargs)
        return self._finalize_response(session, response, 'DELETE')

    def get_request(self, alias, uri, headers=None, params={}, allow_redirects=None, **kwargs):
        """Send a GET request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `headers` a dictionary of headers to use with the request

        `params` a dictionary of key-value pairs that will be urlencoded and sent as GET data

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.get(self._get_url(session, uri), headers=headers, params=self._utf8_urlencode(params),
                               cookies=self.cookies, timeout=self.timeout, allow_redirects=bool(allow_redirects),
                               **kwargs)
        return self._finalize_response(session, response, 'GET')

    def get_session_object(self, alias):
        """Returns the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache
        """
        logger.debug(vars(self._cache.switch(alias)))
        return self._cache.switch(alias)

    def head_request(self, alias, uri, headers=None, allow_redirects=None, **kwargs):
        """Send a HEAD request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the HEAD request to

        `headers` a dictionary of headers to use with the request

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.head(self._get_url(session, uri), headers=headers, cookies=self.cookies,
                                timeout=self.timeout, allow_redirects=bool(allow_redirects), **kwargs)
        return self._finalize_response(session, response, 'HEAD')

    def options_request(self, alias, uri, headers=None, allow_redirects=None, **kwargs):
        """Send a OPTIONS request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the OPTIONS request to

        `headers` a dictionary of headers to use with the request

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.options(self._get_url(session, uri), headers=headers, cookies=self.cookies,
                                   timeout=self.timeout, allow_redirects=bool(allow_redirects), **kwargs)
        return self._finalize_response(session, response, 'OPTIONS')

    def patch_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None, **kwargs):
        """Send a PATCH request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PATCH request to

        `data` a dictionary of key-value pairs that will be urlencoded and sent as PATCH data or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to PATCH to the server

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.patch(self._get_url(session, uri), data=self._utf8_urlencode(data), headers=headers,
                                 files=files, cookies=self.cookies, timeout=self.timeout,
                                 allow_redirects=bool(allow_redirects), **kwargs)
        return self._finalize_response(session, response, 'PATCH')

    def post_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None, **kwargs):
        """Send a POST request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the POST request to

        `data` a dictionary of key-value pairs that will be urlencoded and sent as POST data or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to POST to the server

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.post(self._get_url(session, uri), data=self._utf8_urlencode(data), headers=headers,
                                files=files, cookies=self.cookies, timeout=self.timeout,
                                allow_redirects=bool(allow_redirects), **kwargs)
        return self._finalize_response(session, response, 'POST')

    def put_request(self, alias, uri, data=None, headers=None, allow_redirects=None, **kwargs):
        """Send a PUT request on the session object found in the cache using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PUT request to

        `data` a dictionary of key-value pairs that will be urlencoded and sent as PUT data or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `allow_redirects` a flag to allow connection redirects
        """
        session = self._cache.switch(alias)
        response = session.put(self._get_url(session, uri), data=self._utf8_urlencode(data), headers=headers,
                               cookies=self.cookies, timeout=self.timeout, allow_redirects=bool(allow_redirects),
                               **kwargs)
        return self._finalize_response(session, response, 'PUT')

    def _finalize_response(self, session, response, method):
        # store the last response object
        session.last_resp = response
        self.builtin.log("%s response: %s" % (method, response.content), 'DEBUG')
        return response

    def _register_url(self, url=None):
        host = urlparse(url).hostname
        if host not in self._primers:
            requests.head('%s' % url, verify=False)
            self._primers[host] = 1

    def _register_urls(self, base_url=None, token_url=None):
        self._register_url(base_url)
        self._register_url(token_url)

    def _session_init(self, session=None, base_url=None, headers={}, proxies=None, verify=False, timeout=90,
                      cookies=None):
        # can't use hooks :(
        session.url = base_url
        session.headers.update(headers)
        session.proxies = proxies if proxies else session.proxies
        session.verify = self.builtin.convert_to_boolean(verify)
        # cant pass these into the Session anymore
        self.timeout = timeout
        self.cookies = cookies
        self.verify = verify