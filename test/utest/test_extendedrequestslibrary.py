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

from sys import path
path.append('src')
from ExtendedRequestsLibrary import ExtendedRequestsLibrary
from ExtendedRequestsLibrary.keywords import Utility
from os.path import abspath, dirname
from RequestsLibrary import RequestsLibrary
import mock
import unittest


class ExtendedRequestsLibraryTests(unittest.TestCase):
    """Extended Requests library test class."""

    def setUp(self):
        """Instantiate the extended requests library class."""
        self.alias = 'MY-LABEL'
        self.allow_redirects = None
        self.base_url = 'https://localhost/api'
        self.cookies = None
        self.cwd = abspath(dirname(__file__))
        self.headers = None
        self.library = ExtendedRequestsLibrary()
        self.library._cache = mock.Mock()
        self.password = 'MY-PASSWORD'
        self.proxies = None
        self.tenant_id = 'key'
        self.tenant_secret = 'secret'
        self.timeout = 90
        self.token_url = 'https://localhost/oauth/token'
        self.uri = 'endpoint'
        self.username = 'MY-USERNAME'
        self.value = 'MY-VALUE'
        self.verify = False

    def test_should_inherit_keywords(self):
        """Extended Requests library instance should inherit keyword instances."""
        self.assertIsInstance(self.library, RequestsLibrary)
        self.assertIsInstance(self.library, Utility)

    def method_request_workflow(self, method, mock_oauth2, **kwargs):
        has_files = 'files' in kwargs
        files = kwargs.pop('files', None)
        library = self.library
        oauth2_instance = mock_oauth2()
        library._cache.switch.return_value = oauth2_instance
        library._finalize_response = mock.Mock()
        url = library._get_url(oauth2_instance, self.uri)
        lib_kwargs = {}
        request_kwargs = kwargs.copy()
        request_kwargs['allow_redirects'] = bool(self.allow_redirects)
        request_kwargs['cookies'] = self.cookies
        if method == 'delete' or method == 'put':
            request_kwargs['data'] = None
        if has_files:
            if files is not None:
                lib_kwargs['files'] = files
            request_kwargs['files'] = files
        request_kwargs['headers'] = self.headers
        if method == 'get':
            request_kwargs['params'] = None
        request_kwargs['timeout'] = self.timeout
        getattr(library, '%s_request' % method)(self.alias, self.uri, **lib_kwargs)
        getattr(oauth2_instance, method).assert_called_with(url, **request_kwargs)
        response = getattr(oauth2_instance, method)()
        library._finalize_response.assert_called_with(oauth2_instance, response, method.upper())

    def oauth2_workflow(self, grant, mock_logger, mock_oauth2, mock_client, mock_auth):
        args = [self.alias, self.token_url, self.tenant_id, self.tenant_secret]
        fetch_token_args = {'auth': mock_auth(), 'verify': self.verify}
        kwargs = dict(base_url=self.base_url, cookies=self.cookies, headers=self.headers,
                      proxies=self.proxies, timeout=self.timeout, verify=self.verify)
        library = self.library
        library._register_urls = mock.Mock()
        library._session_init = mock.Mock()
        if grant == 'password':
            args.append(self.username)
            args.append(self.password)
            fetch_token_args['username'] = self.username
            fetch_token_args['password'] = self.password
        method = 'create_%s_oauth2_session' % grant
        oauth2_instance = mock_oauth2()
        getattr(library, method)(*args, **kwargs)
        library._register_urls.assert_called_with(base_url=self.base_url,
                                                  token_url=self.token_url)
        mock_client.assert_called_with('')
        mock_oauth2.assert_called_with(client=mock_client())
        library._session_init.assert_called_with(oauth2_instance, base_url=self.base_url,
                                                 cookies=self.cookies, headers=self.headers,
                                                 proxies=self.proxies, timeout=self.timeout,
                                                 verify=self.verify)
        mock_auth.assert_called_with(self.tenant_id, self.tenant_secret)
        oauth2_instance.fetch_token.assert_called_with(self.token_url, **fetch_token_args)
        library._cache.register.assert_called_with(oauth2_instance, alias=self.alias)

    def test_should_have_default_values(self):
        """Extended Requests library instance should have default values set."""
        self.assertIsInstance(self.library, ExtendedRequestsLibrary)
        self.assertIsInstance(self.library._primers, dict)
        self.assertIsNone(self.library.cookies)
        self.assertEqual(self.library.timeout, self.timeout)
        self.assertFalse(self.library.verify)

    def test_delete_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.delete()
        self.assertTrue("'delete' is deprecated." in context.exception)

    def test_get_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.get()
        self.assertTrue("'get' is deprecated." in context.exception)

    def test_head_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.head()
        self.assertTrue("'head' is deprecated." in context.exception)

    def test_options_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.options()
        self.assertTrue("'options' is deprecated." in context.exception)

    def test_post_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.post()
        self.assertTrue("'post' is deprecated." in context.exception)

    def test_put_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.put()
        self.assertTrue("'put' is deprecated." in context.exception)

    def test_patch_keyword_raise_exception(self):
        with self.assertRaises(AttributeError) as context:
            self.library.patch()
        self.assertTrue("'patch' is deprecated." in context.exception)

    def test_create_session_workflow(self):
        library = self.library
        session = mock.Mock()
        library._cache.switch.return_value = session
        library.create_session(self.alias, self.base_url)
        self.assertEqual(library.get_session_object(self.alias), session)

    def test_create_ntlm_session_workflow(self):
        library = self.library
        session = mock.Mock()
        library._cache.switch.return_value = session
        library.create_ntlm_session(self.alias, self.base_url,
                                    auth=('MY-DOMAIN', self.username, self.password))
        self.assertEqual(library.get_session_object(self.alias), session)

    @mock.patch('ExtendedRequestsLibrary.HTTPBasicAuth')
    @mock.patch('ExtendedRequestsLibrary.BackendApplicationClient')
    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    @mock.patch('ExtendedRequestsLibrary.logger')
    def test_client_oauth2_workflow(self, mock_logger, mock_oauth2, mock_backend, mock_auth):
        self.oauth2_workflow('client', mock_logger, mock_oauth2, mock_backend, mock_auth)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_delete_request_workflow(self, mock_oauth2):
        self.method_request_workflow('delete', mock_oauth2)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_get_request_workflow(self, mock_oauth2):
        self.method_request_workflow('get', mock_oauth2, params=None)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    @mock.patch('ExtendedRequestsLibrary.logger')
    def test_get_session_object_workflow(self, mock_logger, mock_oauth2):
        library = self.library
        oauth2_instance = mock_oauth2()
        library._cache.switch.return_value = oauth2_instance
        library.get_session_object(self.alias)
        library._cache.switch.assert_called_with(self.alias)
        mock_logger.debug.assert_called_with(vars(library._cache.switch()))

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_head_request_workflow(self, mock_oauth2):
        self.method_request_workflow('head', mock_oauth2)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_options_request_workflow(self, mock_oauth2):
        self.method_request_workflow('options', mock_oauth2)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_patch_request_workflow(self, mock_oauth2):
        self.method_request_workflow('patch', mock_oauth2, data=None, files=None)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_post_request_workflow(self, mock_oauth2):
        self.method_request_workflow('post', mock_oauth2, data=None, files=None)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_post_request_workflow_with_files(self, mock_oauth2):
        self.method_request_workflow('post', mock_oauth2, data=None,
                                     files={'file.txt': '%s/file.txt' % self.cwd})

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    def test_put_request_workflow(self, mock_oauth2):
        self.method_request_workflow('put', mock_oauth2, data=None)

    @mock.patch('ExtendedRequestsLibrary.HTTPBasicAuth')
    @mock.patch('ExtendedRequestsLibrary.LegacyApplicationClient')
    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    @mock.patch('ExtendedRequestsLibrary.logger')
    def test_password_oauth2_workflow(self, mock_logger, mock_oauth2, mock_legacy, mock_auth):
        self.oauth2_workflow('password', mock_logger, mock_oauth2, mock_legacy, mock_auth)

    @mock.patch('ExtendedRequestsLibrary.OAuth2Session')
    @mock.patch('ExtendedRequestsLibrary.logger')
    def test_finalize_response(self, mock_logger, mock_oauth2):
        oauth2_instance = mock_oauth2()
        type(oauth2_instance.head()).content = mock.PropertyMock(return_value=self.value)
        response = oauth2_instance.head()
        self.library._finalize_response(oauth2_instance, response, 'HEAD')
        self.assertEqual(oauth2_instance.last_resp, response)
        mock_logger.debug.assert_called_with("%s response: %s" % ('HEAD', self.value))

    @mock.patch('ExtendedRequestsLibrary.requests')
    def test_should_register_url(self, mock_requests):
        hostname = 'subdomain.domain.moo'
        library = self.library
        self.assertFalse(hostname in library._primers)
        library._register_url('http://%s' % hostname)
        mock_requests.head.assert_called_with('http://%s' % hostname, verify=False)
        self.assertTrue(hostname in library._primers)

    def test_should_register_urls(self):
        library = self.library
        library._register_url = mock.Mock()
        library._register_urls(base_url='http://localhost1', token_url='https://localhost2')
        library._register_url.assert_any_call('http://localhost1')
        library._register_url.assert_any_call('https://localhost2')
        self.assertTrue(library._register_url.call_count, 2)

    def test_should_init_session_with_header(self):
        session = mock.Mock()
        self.library._session_init(session, base_url=self.base_url, headers={'key': 'value'},
                                   proxies=self.proxies, verify=self.verify,
                                   timeout=self.timeout, cookies=self.cookies)
        self.assertEqual(session.url, self.base_url)
        session.headers.update.assert_called_with({'key': 'value'})
        self.assertIsNotNone(session.proxies)
        self.assertFalse(session.verify)
        self.assertEqual(self.library.cookies, self.cookies)
        self.assertEqual(self.library.timeout, self.timeout)
        self.assertEqual(self.library.verify, self.verify)

    def test_should_init_session_with_proxy(self):
        session = mock.Mock()
        self.library._session_init(session, base_url=self.base_url, headers=self.headers,
                                   proxies={'key': 'value'}, verify=self.verify,
                                   timeout=self.timeout, cookies=self.cookies)
        self.assertEqual(session.url, self.base_url)
        self.assertFalse(session.headers.update.called)
        self.assertEqual(session.proxies, {'key': 'value'})
        self.assertFalse(session.verify)
        self.assertEqual(self.library.cookies, self.cookies)
        self.assertEqual(self.library.timeout, self.timeout)
        self.assertEqual(self.library.verify, self.verify)

    def test_should_init_session_without_header(self):
        session = mock.Mock()
        self.library._session_init(session, base_url=self.base_url, headers=self.headers,
                                   proxies=self.proxies, verify=self.verify,
                                   timeout=self.timeout, cookies=self.cookies)
        self.assertEqual(session.url, self.base_url)
        self.assertFalse(session.headers.update.called)
        self.assertIsNotNone(session.proxies)
        self.assertFalse(session.verify)
        self.assertEqual(self.library.cookies, self.cookies)
        self.assertEqual(self.library.timeout, self.timeout)
        self.assertEqual(self.library.verify, self.verify)

    def test_should_not_init_without_session(self):
        self.library.cookies = 'yum'
        self.library.timeout = 0
        self.library.verify = True
        self.library._session_init(session=None)
        self.assertEqual(self.library.cookies, 'yum')
        self.assertEqual(self.library.timeout, 0)
        self.assertTrue(self.library.verify)
