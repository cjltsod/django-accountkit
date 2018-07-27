from django.conf import settings
from django.contrib.auth.models import User


class AccountKitAuthenticationBackend:
    def authenticate(self, request, phone=None, email=None):
        phone_prefix = getattr(settings, 'ACCOUNT_KIT_PHONEASUSERNAME_PREFIX', 'fbak_phone_')
        phone_postfix = getattr(settings, 'ACCOUNT_KIT_PHONEASUSERNAME_POSTFIX', '')
        email_prefix = getattr(settings, 'ACCOUNT_KIT_EMAILASUSERNAME_PREFIX', 'fbak_email_')
        email_postfix = getattr(settings, 'ACCOUNT_KIT_EMAILASUSERNAME_POSTFIX', '')
        chk_email_with_username = getattr(settings, 'ACCOUNT_KIT_EMAILASUSERNAME', False)
        auto_create = getattr(settings, 'ACCOUNT_KIT_AUTOCREATE', False)
        try:
            if phone:
                user = User.objects.get(username='{}{}{}'.format(phone_prefix, phone, phone_postfix))
            elif email:
                if chk_email_with_username:
                    user = User.objects.get(username='{}{}{}'.format(email_prefix, email, email_postfix))
                else:
                    user = User.objects.get(email=email)
            else:
                user = None
        except User.DoesNotExist:
            if auto_create:
                if phone:
                    user = User(username='{}{}{}'.format(phone_prefix, phone, phone_postfix))
                elif email:
                    user = User(username='{}{}{}'.format(email_prefix, email, email_postfix), email=email)
                user.save()
            else:
                return None

        user = user if user.is_active else None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
