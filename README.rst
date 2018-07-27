=====================
AccountKit for Django
=====================

Login by Account kit with Django

https://developers.facebook.com/docs/accountkit

Requirement
-----------

- Python (>3.7)
- Django (>2.0)
- Requests (>2.19)
- We only tested on environment as below

Installation
------------

Install through ``pip`` 

.. code-block:: console::

    $ pip install -e git+https://github.com/cjltsod/django-accountkit.git#egg=accountkit
    
Configuration
-------------

Add the following settings in your ``settings.py`` file

.. code-block:: Python

    ACCOUNT_KIT_API_VERSION = 'v1.3'
    ACCOUNT_KIT_APP_ID = '<YOUR_APP_ID_HERE>'
    ACCOUNT_KIT_APP_SECRET = '<YOUR_APP_SECRET_HERE>'

Add ``accountkit`` into your installed apps in your ``settings.py`` file

.. code-block:: Python

    INSTALLED_APPS = [
        'accountkit',
        ......
    ]

Replace authentication backends in your ``settings.py`` file

.. code-block:: Python

    AUTHENTICATION_BACKENDS = (
        'accountkit.authentication.backend.AccountKitAuthenticationBackend',
        'django.contrib.auth.backends.ModelBackend',  # Keep original authentication backends
    )

Add ``accountkit.urls`` into your ``urls.py``

.. code-block:: Python

    from django.urls import include

    urlpatterns = [
        path('acountkit/', include('accountkit.urls')),
        ...
    ]

Customization
-------------

The following settings you can set in your ``settings.py`` are optional

.. code-block:: Python

    ACCOUNT_KIT_LANGUAGE_CODE = 'en_US'
    ACCOUNT_KIT_SUCCESS_REDIRECT = reverse('accountkit_success')
    ACCOUNT_KIT_PHONEASUSERNAME_PREFIX = 'fbak_phone_'
    ACCOUNT_KIT_PHONEASUSERNAME_POSTFIX = ''
    ACCOUNT_KIT_EMAILASUSERNAME_PREFIX = 'fbak_email_'
    ACCOUNT_KIT_EMAILASUSERNAME_POSTFIX = ''
    ACCOUNT_KIT_EMAILASUSERNAME = False
    ACCOUNT_KIT_AUTOCREATE = False

+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| Key                                 | Description                                                                                                                                        | Default                       |
+=====================================+====================================================================================================================================================+===============================+
| ACCOUNT_KIT_LANGUAGE_CODE           | Set the display language. For more supported language code, visit https://developers.facebook.com/docs/accountkit/languages for more information.  | 'en_US'                       |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_SUCCESS_REDIRECT        | The url where handle success after authenticated by AcoountKit.                                                                                    | reverse('accountkit_success') |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_PHONEASUSERNAME_PREFIX  | Prefix of username when using phone as username.                                                                                                   | 'fbak_phone_'                 |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_PHONEASUSERNAME_POSTIX  | Postfix of username when using phone as username.                                                                                                  | ''                            |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_EMAILASUSERNAME_PREFIX  | Prefix of username when using email as username. Only valid when ``ACCOUNT_KIT_EMAILASUSERNAME`` set to ``True``                                   | 'fbak_email_'                 |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_EMAILASUSERNAME_POSTIX  | Postfix of username when using email as username. Only valid when ``ACCOUNT_KIT_EMAILASUSERNAME`` set to ``True``                                  | ''                            |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_EMAILASUSERNAME         | Set to ``True`` if checking username when log in via e-mail, otherwise check e-mail instead.                                                       | False                         |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+
| ACCOUNT_KIT_AUTOCREATE              | Create user if user not exist.                                                                                                                     | False                         |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+


Template Tags
-------------

Load template tags by ``{% load accountkit %}``, then the following template tags can be used in html.

- ``{% accountkitheadjs %}`` : Import AccountKit Javascript SDK. Put this tags inside the HTML ``<head></head>`` tag.
- ``{% accountkitbodyjs %}`` : Javascript that initial AccountKit. Put this tags at the bottom of HTML ``<body></body>`` tags.

You should add HTML elements to trigger AccountKit. Here's the example of html form offered from AccountKit. https://developers.facebook.com/docs/accountkit/webjs

.. code-block:: Django

    <input value="+1" id="country_code" />
    <input placeholder="phone number" id="phone_number"/>
    <button onclick="smsLogin();">Login via SMS</button>
    <div>OR</div>
    <input placeholder="email" id="email"/>
    <button onclick="emailLogin();">Login via Email</button>

Django Admin
------------

If you would like AccountKit to handle login in Django Admin, put ``accountkit`` before ``django.contrib.admin`` in ``settings.py``.

.. code-block:: Python

    INSTALLED_APPS = [
        ......
        'accountkit',
        'django.contrib.admin',
        ......
    ]


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/cjltsod/django-accountkit/issues


License
-------

You can use this under MIT. See `LICENSE <LICENSE>`_ file for details.

Author
------

Developed and maintained by `CJLTSOD <https://about.me/cjltsod/>`_.

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see AUTHORS.rst for a list of contributors.
