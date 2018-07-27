import hashlib
import hmac

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView


def genAppSecretProof(app_secret, access_token):
    h = hmac.new(
        app_secret.encode('utf-8'),
        msg=access_token.encode('utf-8'),
        digestmod=hashlib.sha256,
    )
    return h.hexdigest()


# Create your views here.

class AccountKitSuccessView(RedirectView):
    def post(self, request, *args, **kwargs):
        api_version = getattr(settings, 'ACCOUNT_KIT_API_VERSION')
        secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
        app_id = getattr(settings, 'ACCOUNT_KIT_APP_ID')
        login_redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL')

        code = request.GET.get('code') if request.GET.get('code', None) else request.POST.get('code', None)
        state = request.GET.get('state') if request.GET.get('state', None) else request.POST.get('state', None)
        status = request.GET.get('status') if request.GET.get('status', None) else request.POST.get('status', None)

        authenticated = None
        if request.user.is_authenticated:
            authenticated = True
            messages.add_message(
                request, messages.INFO,
                'User with username {} is already logged in'.format(request.user.username),
            )
        elif status != "PARTIALLY_AUTHENTICATED":
            authenticated = False
            messages.add_message(request, messages.ERROR, 'Accountkit could not authenticate the user')

        '''
        if authenticated is None:
            try:
                signer = TimestampSigner()
                csrf = signer.unsign(state)
            except BadSignature:
                authenticated = False
                messages.add_message(request, messages.ERROR, 'Invalid request')
        '''

        if authenticated is None:
            # Exchange authorization code for access token
            token_url = 'https://graph.accountkit.com/{}/access_token'.format(api_version)
            params = dict(
                grant_type='authorization_code',
                code=code,
                access_token='AA|{}|{}'.format(app_id, secret),
            )

            res = requests.get(token_url, params=params)
            token_response = res.json()

            if 'error' in token_response:
                authenticated = False
                messages.add_message(request, messages.ERROR, 'This authorization code has been used')

        if authenticated is None:
            user_id = token_response.get('id')
            user_access_token = token_response.get('access_token')
            refresh_interval = token_response.get('token_refresh_interval_sec')

            # Get Account Kit information
            identity_url = 'https://graph.accountkit.com/{}/me'.format(api_version)
            identity_params = dict(
                access_token=user_access_token,
                appsecret_proof=genAppSecretProof(secret, user_access_token),
            )

            res = requests.get(identity_url, params=identity_params)
            identity_response = res.json()

            if 'error' in identity_response:
                authenticated = False
                messages.add_message(request, messages.ERROR, identity_response['error']['message'])
            elif identity_response['application']['id'] != app_id:
                authenticated = False
                messages.add_message(request, messages.ERROR,
                                     'The application id returned does not match the one in your settings')

        if authenticated is None:
            if 'email' in identity_response:
                email = identity_response['email']['address']
                user = authenticate(request, email=email)
                if not user:
                    authenticated = False
                    messages.add_message(request, messages.ERROR,
                                         'Please check if the user with email {} is active'.format(email))
            elif 'phone' in identity_response:
                phone = identity_response['phone']['number']
                user = authenticate(request, phone=phone)
                if not user:
                    authenticated = False
                    messages.add_message(request, messages.ERROR,
                                         'Please check if the user with phone {} is active'.format(phone))
            else:
                authenticated = False
                messages.add_message(request, messages.ERROR, 'Invalid request')

        if authenticated is None:
            login(request, user)
            authenticated = True
            messages.add_message(request, messages.SUCCESS, 'User with username {} logged in'.format(user.username))

        self.url = request.POST.get('next') or request.GET.get('next') or login_redirect_url or '/'
        return super(AccountKitSuccessView, self).get(request, *args, **kwargs)
