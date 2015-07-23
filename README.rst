Extended Requests HTTP client testing library for Robot Framework
=================================================================

Introduction
------------

ExtendedRequestsLibrary is an extended HTTP client library for `Robot Framework`_
with OAuth2_ support that leverages the requests_ project,
`requests-oauthlib`_ project, and RequestsLibrary_ project.

More information about this library can be found in the `Keyword Documentation`_.

Example
'''''''

+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| Create Client OAuth2 Session   | client | https://localhost/oauth/token | key | secret | base_url=https://localhost/member                       |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| ${var} = | Post Request        | client | info                          | json=${"key": "value"}                                                 |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| Log      | ${var}                                                                                                                                |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| Create Password OAuth2 Session | member | https://localhost/oauth/token | key | secret | username | password | base_url=https://localhost/member |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| ${var} = | Post Request        | member | info                          | json=${"key": "value"}                                                 |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| Log      | ${var}                                                                                                                                |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+
| Delete All Sessions                                                                                                                              |
+----------+---------------------+--------+-------------------------------+-----+--------+----------+----------+-----------------------------------+

Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using pip_:

.. code:: bash

    pip install robotframework-extendedrequestslibrary

The main benefit of using ``pip`` is that it automatically installs all
dependencies needed by the library. Other nice features are easy upgrading
and support for un-installation:

.. code:: bash

    pip install --upgrade robotframework-extendedrequestslibrary
    pip uninstall robotframework-extendedrequestslibrary

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the requests project used by the library:

.. code:: bash

    pip install robotframework-extendedrequestslibrary==0.1.7
    pip install --upgrade requests
    pip install requests==2.7.0

Proxy configuration
'''''''''''''''''''

If you are behind a proxy, you can use ``--proxy`` command line option
or set ``http_proxy`` and/or ``https_proxy`` environment variables to
configure ``pip`` to use it. If you are behind an authenticating NTLM proxy,
you may want to consider installing CNTML_ to handle communicating with it.

For more information about ``--proxy`` option and using pip with proxies
in general see:

- http://pip-installer.org/en/latest/usage.html
- http://stackoverflow.com/questions/9698557/how-to-use-pip-on-windows-behind-an-authenticating-proxy
- http://stackoverflow.com/questions/14149422/using-pip-behind-a-proxy

Manual installation
'''''''''''''''''''

If you do not have network connection or cannot make proxy to work, you need
to resort to manual installation. This requires installing both the library
and its dependencies yourself.

- Make sure you have `Robot Framework installed`_.

- Download source distributions (``*.tar.gz``) for the library and its dependencies:

  - https://pypi.python.org/pypi/robotframework-extendedrequestslibrary
  - https://pypi.python.org/pypi/robotframework-requestslibrary
  - https://pypi.python.org/pypi/requests-oauthlib
  - https://pypi.python.org/pypi/requests

- Download PGP signatures (``*.tar.gz.asc``) for signed packages.

- Find each public key used to sign the package:

.. code:: bash

    gpg --keyserver pgp.mit.edu --search-keys D1406DE7

- Select the number from the list to import the public key

- Verify the package against its PGP signature:

.. code:: bash

    gpg --verify robotframework-extendedrequestslibrary-0.1.7.tar.gz.asc robotframework-extendedrequestslibrary-0.1.7.tar.gz

- Extract each source distribution to a temporary location.

- Go to each created directory from the command line and install each project using:

.. code:: bash

       python setup.py install

If you are on Windows, and there are Windows installers available for
certain projects, you can use them instead of source distributions.
Just download 32bit or 64bit installer depending on your system,
double-click it, and follow the instructions.

Directory Layout
----------------

doc/
    `Keyword documentation`_

src/
    Python source code

Usage
-----

To write tests with Robot Framework and ExtendedRequestsLibrary,
ExtendedRequestsLibrary must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.

Building Keyword Documentation
------------------------------

The `Keyword Documentation`_ can be found online, if you need to generate the keyword documentation, run:

.. code:: bash

    make doc

License
-------

Copyright (c) 2015 Richard Huang.

This library is free software, licensed under: `GNU Affero General Public License (AGPL-3.0)`_.

Documentation and other similar content are provided under `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License <http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.

.. _CNTML: http://cntlm.sourceforge.net
.. _GNU Affero General Public License (AGPL-3.0): http://www.gnu.org/licenses/agpl-3.0.en.html
.. _Keyword Documentation: https://rickypc.github.io/robotframework-extendedrequestslibrary/doc/ExtendedRequestsLibrary.html
.. _OAuth2: http://oauth.net/2/
.. _pip: http://pip-installer.org
.. _requests: http://docs.python-requests.org/en/latest/
.. _requests-oauthlib: https://requests-oauthlib.readthedocs.org/en/latest/
.. _RequestsLibrary: https://bulkan.github.io/robotframework-requests/
.. _Robot Framework: http://robotframework.org
.. _Robot Framework installed: http://code.google.com/p/robotframework/wiki/Installation
.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuide
