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

import logging
import requests
from ExtendedRequestsLibrary.decorators import inherit_docs
from ExtendedRequestsLibrary.keywords import Utility
from ExtendedRequestsLibrary.version import get_version
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from RequestsLibrary import RequestsLibrary
from robot.api import logger
requests.packages.urllib3.disable_warnings()
logging.getLogger('requests').setLevel(logging.WARNING)

try:
    from urllib.parse import urlparse  # pylint: disable=no-name-in-module
except ImportError:
    from urlparse import urlparse  # pylint: disable=no-name-in-module

__version__ = get_version()


@inherit_docs
class ExtendedRequestsLibrary(RequestsLibrary, Utility):
    # pylint: disable=line-too-long
    """ExtendedRequestsLibrary is an extended  HTTP client library
    for Robot Framework with OAuth2 support that leverages other projects:
    requests project, requests_oauthlib project, and RequestsLibrary project.

    *Non-inherited Keywords*
    | `Create Client OAuth2 Session`   |
    | `Create Password OAuth2 Session` |
    | `Get JSON File`                  |
    | `Get Session Object`             |
    | `JSON Loads`                     |

    *Inherited Deprecated Keywords*
    | `Delete`  |
    | `Get`     |
    | `Head`    |
    | `Options` |
    | `Patch`   |
    | `Post`    |
    | `Put`     |
    | `To Json` |

    Examples:
    | Create Client OAuth2 Session | client | https://localhost/oauth/token | key | secret | base_url=https://localhost/member |
    | ${var} = | Post Request | client | info | json=${"key": "value"} |
    | Log | ${var} |
    | Create Password OAuth2 Session | member | https://localhost/oauth/token | key | secret | username | password | base_url=https://localhost/member |
    | ${var} = | Post Request | member | info | json=${"key": "value"} |
    | Log | ${var} |
    | Delete All Sessions |

    Example for File Upload:
    | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
    | Create Client OAuth2 Session | client | https://localhost/oauth/token | key | secret | base_url=https://localhost/member |
    | ${var} = | Post Request | client | info | files=&{files} |
    | Log | ${var} |
    """
    # pylint: disable=line-too-long

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    # pylint: disable=super-init-not-called
    def __init__(self):
        """Extended Request Library class init.

        Examples:
        | Library | ExtendedRequestsLibrary |
        """
        for base in ExtendedRequestsLibrary.__bases__:
            base.__init__(self)
        self._primers = {}
        self.cookies = None
        self.timeout = 90
        self.verify = False

    def __getattribute__(self, name):
        """Returns requested attribute."""
        if name in ('delete', 'get', 'head', 'options', 'patch', 'post', 'put', 'to_json'):
            raise AttributeError("'%s' is deprecated." % name)
        return super(ExtendedRequestsLibrary, self).__getattribute__(name)

    def create_client_oauth2_session(self, *args, **kwargs):
        # pylint: disable=line-too-long
        """Create and return an OAuth2 session to a server with client credentials grant
        access token.

        ``alias`` is a Robot Framework alias to identify the OAuth2 session

        ``token_url`` is url of the OAuth2 token server

        ``tenant_id`` is the client id obtained during registration with OAuth2 provider

        ``tenant_secret`` is the client secret obtained during registration with OAuth2 provider

        ``base_url`` is base url of the server

        ``headers`` is a Dictionary of default headers

        ``cookies`` is a Dictionary of default cookies

        ``timeout`` is the connection timeout in seconds

        ``proxies`` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create Client OAuth2 Session | My-Label | https://localhost/oauth/token |
        | ${var} = | Create Client OAuth2 Session | My-Label | https://localhost/oauth/token | key | secret |
        """
        # pylint: disable=line-too-long
        return self._create_oauth2_session(BackendApplicationClient(''), *args, **kwargs)

    def create_ntlm_session(self, alias, url, auth, **kwargs):
        super(ExtendedRequestsLibrary, self).create_ntlm_session(alias, url, auth, **kwargs)

    def create_password_oauth2_session(self, *args, **kwargs):
        # pylint: disable=line-too-long
        """Create and return an OAuth2 session to a server with password grant
        access token.

        ``alias`` is a Robot Framework alias to identify the OAuth2 session

        ``token_url`` is url of the OAuth2 token server

        ``tenant_id`` is the client id obtained during registration with OAuth2 provider

        ``tenant_secret`` is the client secret obtained during registration with OAuth2 provider

        ``username`` is the resource owner username

        ``password`` is the resource owner password

        ``base_url`` is base url of the server

        ``headers`` is a Dictionary of default headers

        ``cookies`` is a Dictionary of default cookies

        ``timeout`` is the connection timeout in seconds

        ``proxies`` is a Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` set to True if Requests should verify the SSL certificate

        Examples:
        | ${var} = | Create Password OAuth2 Session | My-Label | https://localhost/oauth/token |
        | ${var} = | Create Password OAuth2 Session | My-Label | https://localhost/oauth/token | key | secret |
        | ${var} = | Create Password OAuth2 Session | My-Label | https://localhost/oauth/token | username=username | password=password |
        | ${var} = | Create Password OAuth2 Session | My-Label | https://localhost/oauth/token | key | secret | username | password |
        """
        # pylint: disable=line-too-long
        return self._create_oauth2_session(LegacyApplicationClient(''), *args, **kwargs)

    def create_session(self, alias, url, **kwargs):
        super(ExtendedRequestsLibrary, self).create_session(alias, url, **kwargs)

    def delete_request(self, alias, uri, **kwargs):
        """Send a DELETE request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the DELETE request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and
        sent as DELETE data or binary data that is sent as the raw body content

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` a flag to allow connection redirects
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.delete(self._get_url(session, uri), allow_redirects=allow_redirects,
                                  cookies=self.cookies, data=data, headers=headers,
                                  timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'DELETE')

    def get_request(self, alias, uri, **kwargs):
        """Send a GET request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the GET request to

        ``headers`` a dictionary of headers to use with the request

        ``params`` a dictionary of key-value pairs that will be urlencoded and sent as GET data

        ``allow_redirects`` a flag to allow connection redirects
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        params = self._utf8_urlencode(kwargs.pop('params', None))
        session = self._cache.switch(alias)
        response = session.get(self._get_url(session, uri), allow_redirects=allow_redirects,
                               cookies=self.cookies, headers=headers, params=params,
                               timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'GET')

    def get_session_object(self, alias):
        """Returns the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache
        """
        response = self._cache.switch(alias)
        logger.debug(vars(response))
        return response

    def head_request(self, alias, uri, **kwargs):
        """Send a HEAD request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the HEAD request to

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` a flag to allow connection redirects
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.head(self._get_url(session, uri), allow_redirects=allow_redirects,
                                cookies=self.cookies, headers=headers, timeout=self.timeout,
                                **kwargs)
        return self._finalize_response(session, response, 'HEAD')

    def options_request(self, alias, uri, **kwargs):
        """Send a OPTIONS request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the OPTIONS request to

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` a flag to allow connection redirects
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.options(self._get_url(session, uri), allow_redirects=allow_redirects,
                                   cookies=self.cookies, headers=headers, timeout=self.timeout,
                                   **kwargs)
        return self._finalize_response(session, response, 'OPTIONS')

    def patch_request(self, alias, uri, **kwargs):
        # pylint: disable=line-too-long
        """Send a PATCH request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PATCH request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and
        sent as PATCH data or binary data that is sent as the raw body content

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of multiple file names and file paths data to PATCH to the server.

        ``allow_redirects`` a flag to allow connection redirects

        Examples:
        | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
        | ${var} = | Patch Request | label | uri | files=&{files} |
        """
        # pylint: disable=line-too-long
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        files = kwargs.pop('files', None)
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.patch(self._get_url(session, uri), allow_redirects=allow_redirects,
                                 cookies=self.cookies, data=data, files=files, headers=headers,
                                 timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'PATCH')

    def post_request(self, alias, uri, **kwargs):
        # pylint: disable=line-too-long
        """Send a POST request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the POST request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and
        sent as POST data or binary data that is sent as the raw body content

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of multiple file names and file paths data to POST to the server.

        ``allow_redirects`` a flag to allow connection redirects

        Examples:
        | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
        | ${var} = | Post Request | label | uri | files=&{files} |
        """
        # pylint: disable=line-too-long
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        files = kwargs.pop('files', None)
        if files is not None:
            for key, value in files.items():
                files[key] = open(value, 'rb')
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.post(self._get_url(session, uri), allow_redirects=allow_redirects,
                                cookies=self.cookies, data=data, files=files, headers=headers,
                                timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'POST')

    def put_request(self, alias, uri, **kwargs):
        """Send a PUT request on the session object found in the cache using the given ``alias``

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PUT request to

        ``data`` a dictionary of key-value pairs that will be urlencoded and
        sent as PUT data or binary data that is sent as the raw body content

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` a flag to allow connection redirects
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(alias)
        response = session.put(self._get_url(session, uri), allow_redirects=allow_redirects,
                               cookies=self.cookies, data=data, headers=headers,
                               timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'PUT')

    def _create_oauth2_session(self, client, *args, **kwargs):
        """Create and return an OAuth2 session to a server."""
        fetch_kwargs = kwargs.copy()
        kargs = dict(enumerate(args))
        argv = {
            'alias': kargs.get(0, None),
            'password': kargs.get(5, kwargs.get('password', None)),
            'tenant_id': kargs.get(2, None),
            'tenant_secret': kargs.get(3, None),
            'token_url': kargs.get(1, None),
            'username': kargs.get(4, kwargs.get('username', None))
        }
        kw_message = ', '.join(['%s=%s' % (key, value) for (key, value) in list(kwargs.items())])
        log_message = ('Creating OAuth2 Session using: alias=%s, token_url=%s' %
                       (argv.get('alias'), argv.get('token_url')))
        if argv.get('tenant_id') is not None and argv.get('tenant_secret') is not None:
            fetch_kwargs['auth'] = HTTPBasicAuth(argv.get('tenant_id'), argv.get('tenant_secret'))
            log_message += (', tenant_id=%s, tenant_secret=%s' %
                            (argv.get('tenant_id'), argv.get('tenant_secret')))
        if argv.get('username') is not None and argv.get('password') is not None:
            fetch_kwargs['username'] = argv.get('username')
            fetch_kwargs['password'] = argv.get('password')
            log_message += (', username=%s, password=%s' %
                            (argv.get('username'), argv.get('password')))
        if kw_message:
            log_message += ', %s' % kw_message
        logger.debug(log_message)
        self._register_urls(base_url=kwargs.get('base_url', None), token_url=argv.get('token_url'))
        session = OAuth2Session(client=client)
        self._session_init(session, **kwargs)
        fetch_kwargs.pop('base_url', None)
        fetch_kwargs.pop('cookies', None)
        fetch_kwargs.pop('headers', None)
        fetch_kwargs.pop('proxies', None)
        fetch_kwargs.pop('timeout', None)
        session.fetch_token(argv.get('token_url'), **fetch_kwargs)
        self._cache.register(session, alias=argv.get('alias'))
        return session

    @staticmethod
    def _finalize_response(session, response, method):
        """Store last response object, logging, and return the response"""
        session.last_resp = response
        logger.debug("%s response: %s" % (method, response.content))
        return response

    def _register_url(self, url=None):
        """Make HEAD request to warm up the destination server"""
        host = urlparse(url).hostname
        if host not in self._primers:
            requests.head('%s' % url, verify=False)
            self._primers[host] = 1

    def _register_urls(self, base_url=None, token_url=None):
        """Make HEAD requests for both base URL and token URL"""
        self._register_url(base_url)
        self._register_url(token_url)

    def _session_init(self, session=None, **kwargs):
        """Initialize session"""
        if session is None:
            return
        # can't use hooks :(
        headers = kwargs.get('headers', None)
        proxies = kwargs.get('proxies', None)
        session.url = kwargs.get('base_url', None)
        if headers is not None:
            session.headers.update(headers)
        session.proxies = proxies if proxies is not None else session.proxies
        session.verify = self.builtin.convert_to_boolean(kwargs.get('verify', None))
        # cant pass these into the Session anymore
        self.cookies = kwargs.get('cookies', None)
        self.timeout = kwargs.get('timeout', 90)
        self.verify = kwargs.get('verify', False)
