Extended Requests HTTP client testing library for Robot Framework
=================================================================

|Build| |Coverage| |Grade| |Docs| |Version| |Status| |Python| |Download| |License|

Introduction
------------

ExtendedRequestsLibrary is an extended HTTP client library for `Robot Framework`_
with OAuth2_ support that leverages the requests_ project,
`requests-oauthlib`_ project, and RequestsLibrary_ project.

More information about this library can be found in the `Keyword Documentation`_.

Example
'''''''

+----------------------------------+--------+---------------+-----+--------+-----------------------------------------+
| Create Client OAuth2 Session     | client | https://token | key | secret | base_url=https://service                |
+------------+---------------------+--------+---------------+-----+--------+-----------------------------------------+
| ${var} =   | Post Request        | client | /endpoint     | json=${“key": "value"}                                 |
+------------+---------------------+--------+---------------+--------------------------------------------------------+
| Log        | ${var}                                                                                                |
+------------+---------------------+--------+---------------+-----+--------+-----+-----+-----------------------------+
| Create Password OAuth2 Session   | member | https://token | key | secret | usn | pwd | base_url=https://service    |
+------------+---------------------+--------+---------------+-----+--------+-----+-----+-----------------------------+
| ${var} =   | Post Request        | member | /endpoint     | json=${“key": "value"}                                 |
+------------+---------------------+--------+---------------+--------------------------------------------------------+
| Log        | ${var}                                                                                                |
+------------+---------------------+------------------------------+--------------------------------------------------+
| &{files} = | Create Dictionary   | file1=/path/to/a_file.ext    | file2=/path/to/another_file.ext                  |
+------------+---------------------+--------+---------------------+--------------------------------------------------+
| ${var} =   | Post Request        | member | /endpoint           | files=&{files}                                   |
+------------+---------------------+--------+---------------------+--------------------------------------------------+
| Log        | ${var}                                                                                                |
+------------+-------------------------------------------------------------------------------------------------------+
| Delete All Sessions                                                                                                |
+--------------------------------------------------------------------------------------------------------------------+

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

    pip install robotframework-extendedrequestslibrary==x.x.x
    pip install --upgrade requests
    pip install requests==x.x.x

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

    gpg --verify robotframework-extendedrequestslibrary-x.x.x.tar.gz.asc robotframework-extendedrequestslibrary-x.x.x.tar.gz

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

test/
     Test files

     utest/
           Python unit test

Usage
-----

To write tests with Robot Framework and ExtendedRequestsLibrary,
ExtendedRequestsLibrary must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.

More information about Robot Framework standard libraries and built-in tools
can be found in the `Robot Framework Documentation`_.

Building Keyword Documentation
------------------------------

The `Keyword Documentation`_ can be found online, if you need to generate the keyword documentation, run:

.. code:: bash

    make doc

Run Unit Tests, and Test Coverage Report
----------------------------------------

Test the testing library, talking about dogfooding, let's run:

.. code:: bash

    make test

Contributing
------------

If you would like to contribute code to Extended Requests Library project you can do so through GitHub by forking the           repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible. Please also include appropriate test cases.

Before your code can be accepted into the project you must also sign the `Extended Requests Library CLA`_ (Individual Contributor License Agreement).

That's it! Thank you for your contribution!

License
-------

Copyright (c) 2015 Richard Huang.

This library is free software, licensed under: `GNU Affero General Public License (AGPL-3.0)`_.

Documentation and other similar content are provided under `Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License`_.

.. _CNTML: http://cntlm.sourceforge.net
.. _Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License: http://creativecommons.org/licenses/by-nc-sa/4.0/
.. _Extended Requests Library CLA: https://goo.gl/forms/hLzGj1hyWf
.. _GNU Affero General Public License (AGPL-3.0): http://www.gnu.org/licenses/agpl-3.0.en.html
.. _Keyword Documentation: https://rickypc.github.io/robotframework-extendedrequestslibrary/doc/ExtendedRequestsLibrary.html
.. _OAuth2: http://oauth.net/2/
.. _pip: http://pip-installer.org
.. _requests: http://docs.python-requests.org/en/latest/
.. _requests-oauthlib: https://requests-oauthlib.readthedocs.org/en/latest/
.. _RequestsLibrary: https://bulkan.github.io/robotframework-requests/
.. _Robot Framework: http://robotframework.org
.. _Robot Framework Documentation: http://robotframework.org/robotframework/
.. _Robot Framework installed: http://code.google.com/p/robotframework/wiki/Installation
.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuide
.. |Build| image:: https://img.shields.io/travis/rickypc/robotframework-extendedrequestslibrary.svg
    :target: https://travis-ci.org/rickypc/robotframework-extendedrequestslibrary
    :alt: Build Status
.. |Coverage| image:: https://img.shields.io/codecov/c/github/rickypc/robotframework-extendedrequestslibrary.svg
    :target: https://codecov.io/github/rickypc/robotframework-extendedrequestslibrary
    :alt: Code Coverage
.. |Grade| image:: https://img.shields.io/codacy/25e0956bfabc47428dcb19582e8d7a0a.svg
    :target: https://www.codacy.com/app/rickypc/robotframework-extendedrequestslibrary
    :alt: Code Grade
.. |Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://rickypc.github.io/robotframework-extendedrequestslibrary/doc/ExtendedRequestsLibrary.html
    :alt: Keyword Documentation
.. |Version| image:: https://img.shields.io/pypi/v/robotframework-extendedrequestslibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-extendedrequestslibrary
    :alt: Package Version
.. |Status| image:: https://img.shields.io/pypi/status/robotframework-extendedrequestslibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-extendedrequestslibrary
    :alt: Development Status
.. |Python| image:: https://img.shields.io/pypi/pyversions/robotframework-extendedrequestslibrary.svg
    :target: https://www.python.org/downloads/
    :alt: Python Version
.. |Download| image:: https://img.shields.io/pypi/dm/robotframework-extendedrequestslibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-extendedrequestslibrary
    :alt: Monthly Download
.. |License| image:: https://img.shields.io/pypi/l/robotframework-extendedrequestslibrary.svg
    :target: https://www.gnu.org/licenses/agpl-3.0.en.html
    :alt: License
