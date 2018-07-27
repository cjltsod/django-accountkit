# django-accountkit

**Login by Account kit with Django**  https://developers.facebook.com/docs/accountkit

## Requirement

- Python (3.7)
- Django (2.0)

## Installation

Install through ``pip`` 

    pip install -e git+https://github.com/cjltsod/django-accountkit.git
    
## Configuration

Add the following settings in your `settings.py` file

    ACCOUNT_KIT_API_VERSION = 'v1.3'
    ACCOUNT_KIT_APP_ID = '<YOUR_APP_ID_HERE>'
    ACCOUNT_KIT_APP_SECRET = '<YOUR_APP_SECRET_HERE>'

Add `AccountKit` into your installed apps in your `settings.py` file
    
    INSTALLED_APPS = [
        'AccountKit',
        ......
    ]

Replace authentication backends in your `settings.py` file

    AUTHENTICATION_BACKENDS = (
        'AccountKit.authentication.backend.AccountKitAuthenticationBackend',
        'django.contrib.auth.backends.ModelBackend',  # Keep original authentication backends
    )

## Customization

The following settings you can set in your `settings.py` are optional

    ACCOUNT_KIT_LANGUAGE_CODE = 'en_US'
    ACCOUNT_KIT_SUCCESS_REDIRECT = reverse('accountkit_success')
    ACCOUNT_KIT_PHONEASUSERNAME_PREFIX = 'fbak_phone_'
    ACCOUNT_KIT_PHONEASUSERNAME_POSTFIX = ''
    ACCOUNT_KIT_EMAILASUSERNAME_PREFIX = 'fbak_email_'
    ACCOUNT_KIT_EMAILASUSERNAME_POSTFIX = ''
    ACCOUNT_KIT_EMAILASUSERNAME = False
    ACCOUNT_KIT_AUTOCREATE = False

- **ACCOUNT_KIT_LANGUAGE_CODE** : Set the display language. For more supported language code, visit https://developers.facebook.com/docs/accountkit/languages for more information.
- **ACCOUNT_KIT_SUCCESS_REDIRECT** : The url where handle success after authenticated by AcoountKit.
- **ACCOUNT_KIT_PHONEASUSERNAME_PREFIX** : Prefix of username when using phone as username.
- **ACCOUNT_KIT_PHONEASUSERNAME_POSTIX** : Postfix of username when using phone as username.
- **ACCOUNT_KIT_EMAILASUSERNAME_PREFIX** : Prefix of username when using email as username. Only valid when `ACCOUNT_KIT_EMAILASUSERNAME` set to `True`
- **ACCOUNT_KIT_EMAILASUSERNAME_POSTIX** : Postfix of username when using email as username. Only valid when `ACCOUNT_KIT_EMAILASUSERNAME` set to `True`
- **ACCOUNT_KIT_EMAILASUSERNAME** : Set to `True` if checking username when log in via e-mail, otherwise check e-mail instead.
- **ACCOUNT_KIT_AUTOCREATE** : Create user if user not exist.

## Template Tags

Load template tags by `{% load accountkit %}`, then the following template tags can be used in html.
- **`{% accountkitheadjs %}`** : Import AccountKit Javascript SDK. Put this tags inside the HTML `<head></head>` tag.
- **`{% accountkitbodyjs %}`** : Javascript that initial AccountKit. Put this tags at the bottom of HTML `<body></body>` tags.

You should add HTML elements to trigger AccountKit. Here's the example of html form offered from AccountKit. https://developers.facebook.com/docs/accountkit/webjs

    <input value="+1" id="country_code" />
    <input placeholder="phone number" id="phone_number"/>
    <button onclick="smsLogin();">Login via SMS</button>
    <div>OR</div>
    <input placeholder="email" id="email"/>
    <button onclick="emailLogin();">Login via Email</button>

## Django Admin

If you would like AccountKit to handle login in Django Admin, put `AccountKit` before `django.contrib.admin` in `settings.py`.
    
    INSTALLED_APPS = [
        ......
        'AccountKit',
        'django.contrib.admin',
        ......
    ]
