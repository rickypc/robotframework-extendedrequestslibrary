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

try:
    # pylint: disable=no-name-in-module
    from urllib.parse import urlparse
except ImportError:
    # pylint: disable=import-error
    # pylint: disable=no-name-in-module
    from urlparse import urlparse
import logging
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from RequestsLibrary import RequestsLibrary
from robot.api import logger
from ExtendedRequestsLibrary.keywords import Utility
from ExtendedRequestsLibrary.version import get_version

requests.packages.urllib3.disable_warnings()
logging.getLogger('requests').setLevel(logging.WARNING)
__version__ = get_version()


class ExtendedRequestsLibrary(RequestsLibrary, Utility):
    # pylint: disable=line-too-long
    """ExtendedRequestsLibrary is an extended HTTP client library for
    [http://goo.gl/lES6WM|Robot Framework] with [http://goo.gl/VehoOR|OAuth2] support
    that leverages other projects:
    - [http://goo.gl/8p7MOG|requests] project
    - [https://goo.gl/Tavax4|requests_oauthlib] project
    - [https://goo.gl/3FBo9w|RequestsLibrary] project

    Examples:
    | `Create Client OAuth2 Session` | client-label | https://token | key | secret | base_url=https://service |
    | ${var} = | `Post Request` | client-label | /endpoint | json=${"key": "value"} |
    | Log | ${var} |
    | `Create Password OAuth2 Session` | member-label | https://token | key | secret | usn | pwd | base_url=https://service |
    | ${var} = | `Post Request` | member-label | /endpoint | json=${"key": "value"} |
    | Log | ${var} |
    | `Delete All Sessions` |

    Example for File Upload:
    | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
    | `Create Client OAuth2 Session` | label | https://token | key | secret | base_url=https://service |
    | ${var} = | `Post Request` | label | /endpoint | files=&{files} |
    | Log | ${var} |

    Non-inherited Keywords:
    | `Create Client OAuth2 Session`      |
    | `Create Password OAuth2 Session`    |
    | `Get JSON File`                     |
    | `Get Session Object`                |
    | `JSON Loads`                        |
    | `Natural Sort List Of Dictionaries` |

    Inherited Deprecated Keywords:
    | `Delete`  |
    | `Get`     |
    | `Head`    |
    | `Options` |
    | `Patch`   |
    | `Post`    |
    | `Put`     |
    | `To Json` |
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
        """Create and return an [http://goo.gl/VehoOR|OAuth2] session object to a server
        with [https://goo.gl/EJsqun|client credentials] authorization grant
        [https://goo.gl/YjNlJf|access token].

        Arguments:
        - ``label``: A case and space insensitive string to identify the OAuth2 session.
        - ``token_url``: The OAuth2 token server URL.
        - ``tenant_id``: The client id obtained during registration with OAuth2 provider.
        - ``tenant_secret``: The client secret obtained during registration with OAuth2 provider.
        - ``base_url``: The server base URL.
        - ``headers``: Default headers dictionary.
        - ``cookies``: Default cookies dictionary.
        - ``timeout``: The connection timeout in seconds.
        - ``proxies``: The proxy URLs dictionary for HTTP and/or HTTPS communication.
        - ``verify``: Set to True if [http://goo.gl/8p7MOG|Requests] should verify the SSL
                      certificate.

        Examples:
        | ${var} = | Create Client OAuth2 Session | label | https://token |
        | ${var} = | Create Client OAuth2 Session | label | https://token | key | secret |
        """
        return self._create_oauth2_session(BackendApplicationClient(''), *args, **kwargs)

    def create_ntlm_session(self, label, base_url, auth, **kwargs):
        """Create and return a [https://goo.gl/zac4cn|NTLM] session object to a server.

        Arguments:
        - ``label``: A case and space insensitive string to identify the OAuth2 session.
        - ``base_url``: The server base URL.
        - ``auth``: A list of NTLM authentication credentials. ['domain', 'username', 'password']
        - ``headers``: Default headers dictionary.
        - ``timeout``: The connection timeout in seconds.
        - ``proxies``: The proxy URLs dictionary for HTTP and/or HTTPS communication.
        - ``verify``: Set to True if [http://goo.gl/8p7MOG|Requests] should verify the SSL
                      certificate.

        Examples:
        | @{auth} = | Create List | domain | username | password |
        | ${var} = | Create NTLM Session | label | https://service | auth=@{auth} |
        """
        return super(ExtendedRequestsLibrary, self).create_ntlm_session(label, base_url, auth, **kwargs)

    def create_password_oauth2_session(self, *args, **kwargs):
        # pylint: disable=line-too-long
        """Create and return an [http://goo.gl/VehoOR|OAuth2] session object to a server with
        [https://goo.gl/N9R62O|resource owner password credentials] authorization grant
        [https://goo.gl/YjNlJf|access token].

        Arguments:
        - ``label``: A case and space insensitive string to identify the OAuth2 session.
        - ``token_url``: The OAuth2 token server URL.
        - ``tenant_id``: The client id obtained during registration with OAuth2 provider.
        - ``tenant_secret``: The client secret obtained during registration with OAuth2 provider.
        - ``username``: The resource owner username.
        - ``password``: The resource owner password.
        - ``base_url``: The server base URL.
        - ``headers``: Default headers dictionary.
        - ``cookies``: Default cookies dictionary.
        - ``timeout``: The connection timeout in seconds.
        - ``proxies``: The proxy URLs dictionary for HTTP and/or HTTPS communication.
        - ``verify``: Set to True if [http://goo.gl/8p7MOG|Requests] should verify the SSL
                      certificate.

        Examples:
        | ${var} = | Create Password OAuth2 Session | label | https://token |
        | ${var} = | Create Password OAuth2 Session | label | https://token | key | secret |
        | ${var} = | Create Password OAuth2 Session | label | https://token | username=usn | password=pwd |
        | ${var} = | Create Password OAuth2 Session | label | https://token | key | secret | usn | pwd |
        """
        # pylint: disable=line-too-long
        return self._create_oauth2_session(LegacyApplicationClient(''), *args, **kwargs)

    def create_session(self, label, base_url, **kwargs):
        """Create and return a HTTP session object to a server.

        Arguments:
        - ``label``: A case and space insensitive string to identify the OAuth2 session.
        - ``base_url``: The server base URL.
        - ``auth``: A list of HTTP basic authentication credentials. ['username', 'password']
        - ``headers``: Default headers dictionary.
        - ``timeout``: The connection timeout in seconds.
        - ``proxies``: The proxy URLs dictionary for HTTP and/or HTTPS communication.
        - ``verify``: Set to True if [http://goo.gl/8p7MOG|Requests] should verify the SSL
                      certificate.

        Examples:
        | @{auth} = | Create List | username | password |
        | ${var} = | Create Session | label | https://service | auth=@{auth} |
        """
        return super(ExtendedRequestsLibrary, self).create_session(label, base_url, **kwargs)

    def delete_request(self, label, uri, **kwargs):
        """Send a DELETE request on the session object found in the cache using the given
        ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify the Session object
                     in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``data``: A key-value pairs dictionary that will be urlencoded and
                    sent as raw body content data or binary data.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | ${var} = | Delete Request | label | /endpoint |
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.delete(self._get_url(session, uri), allow_redirects=allow_redirects,
                                  cookies=self.cookies, data=data, headers=headers,
                                  timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'DELETE')

    def delete_session(self, label):
        """Removes session object using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.

        Examples:
        | Delete Session | label |
        """
        self._cache.switch(label)
        index = self._cache.current_index
        # pylint: disable=protected-access
        self._cache.current = self._cache._no_current
        # pylint: disable=protected-access
        self._cache._connections[index - 1] = None
        # pylint: disable=protected-access
        self._cache._aliases['x-%s-x' % label] = self._cache._aliases.pop(label)

    def get_request(self, label, uri, **kwargs):
        """Send a GET request on the session object found in the cache using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``params``: A key-value pairs dictionary that will be urlencoded and sent as GET data.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | ${var} = | Get Request | label | /endpoint |
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        params = self._utf8_urlencode(kwargs.pop('params', None))
        session = self._cache.switch(label)
        response = session.get(self._get_url(session, uri), allow_redirects=allow_redirects,
                               cookies=self.cookies, headers=headers, params=params,
                               timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'GET')

    def get_session_object(self, label):
        """Returns the session object found in the cache using the given ``label``

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.

        Examples:
        | ${var} = | Get Session Object | label |
        """
        response = self._cache.switch(label)
        logger.debug(vars(response))
        return response

    def head_request(self, label, uri, **kwargs):
        """Send a HEAD request on the session object found in the cache using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | ${var} = | Head Request | label | /endpoint |
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.head(self._get_url(session, uri), allow_redirects=allow_redirects,
                                cookies=self.cookies, headers=headers, timeout=self.timeout,
                                **kwargs)
        return self._finalize_response(session, response, 'HEAD')

    def options_request(self, label, uri, **kwargs):
        """Send a OPTIONS request on the session object found in the cache
        using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | ${var} = | Options Request | label | /endpoint |
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.options(self._get_url(session, uri), allow_redirects=allow_redirects,
                                   cookies=self.cookies, headers=headers, timeout=self.timeout,
                                   **kwargs)
        return self._finalize_response(session, response, 'OPTIONS')

    def patch_request(self, label, uri, **kwargs):
        # pylint: disable=line-too-long
        """Send a PATCH request on the session object found in the cache
        using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``data``: A key-value pairs dictionary that will be urlencoded and
                    sent as raw body content data or binary data.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``files``: Multiple file names and file paths dictionary data to be uploaded.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
        | ${var} = | Patch Request | label | /endpoint | files=&{files} |
        """
        # pylint: disable=line-too-long
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        files = kwargs.pop('files', None)
        if files is not None:
            for key, value in list(files.items()):
                files[key] = open(value, 'rb')
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.patch(self._get_url(session, uri), allow_redirects=allow_redirects,
                                 cookies=self.cookies, data=data, files=files, headers=headers,
                                 timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'PATCH')

    def post_request(self, label, uri, **kwargs):
        # pylint: disable=line-too-long
        """Send a POST request on the session object found in the cache using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``data``: A key-value pairs dictionary that will be urlencoded and
                    sent as raw body content data or binary data.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``files``: Multiple file names and file paths dictionary data to be uploaded.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | &{files} = | Create Dictionary | file1=/path/to/a_file.ext | file2=/path/to/another_file.ext | # Collections library |
        | ${var} = | Post Request | label | /endpoint | files=&{files} |
        """
        # pylint: disable=line-too-long
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        files = kwargs.pop('files', None)
        if files is not None:
            for key, value in list(files.items()):
                files[key] = open(value, 'rb')
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.post(self._get_url(session, uri), allow_redirects=allow_redirects,
                                cookies=self.cookies, data=data, files=files, headers=headers,
                                timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'POST')

    def put_request(self, label, uri, **kwargs):
        """Send a PUT request on the session object found in the cache using the given ``label``.

        Arguments:
        - ``label``: A case and space insensitive string to identify
                     the Session object in the cache.
        - ``uri``: The request URI that will be combined with ``base_url``
                   if it was specified in the Session object.
        - ``data``: A key-value pairs dictionary that will be urlencoded and
                    sent as raw body content data or binary data.
        - ``headers``: Headers dictionary that will be accompanied the request.
        - ``allow_redirects``: A flag to allow connection redirects.

        Examples:
        | ${var} = | Put Request | label | /endpoint |
        """
        allow_redirects = bool(kwargs.pop('allow_redirects', None))
        data = self._utf8_urlencode(kwargs.pop('data', None))
        headers = kwargs.pop('headers', None)
        session = self._cache.switch(label)
        response = session.put(self._get_url(session, uri), allow_redirects=allow_redirects,
                               cookies=self.cookies, data=data, headers=headers,
                               timeout=self.timeout, **kwargs)
        return self._finalize_response(session, response, 'PUT')

    def _create_oauth2_session(self, client, *args, **kwargs):
        """Create and return an OAuth2 session to a server."""
        fetch_kwargs = kwargs.copy()
        kargs = dict(enumerate(args))
        argv = {
            'label': kargs.get(0, None),
            'password': kargs.get(5, kwargs.pop('password', None)),
            'tenant_id': kargs.get(2, None),
            'tenant_secret': kargs.get(3, None),
            'token_url': kargs.get(1, None),
            'username': kargs.get(4, kwargs.pop('username', None))
        }
        kw_message = ', '.join(['%s=%s' % (key, value) for (key, value) in list(kwargs.items())])
        log_message = ('Creating OAuth2 Session using: label=%s, token_url=%s' %
                       (argv.get('label'), argv.get('token_url')))
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
        self._cache.register(session, alias=argv.get('label'))
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
