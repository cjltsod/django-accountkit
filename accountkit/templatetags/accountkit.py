from django.conf import settings
from django.core.signing import TimestampSigner
from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()

accountkit_api_version = getattr(settings, 'ACCOUNT_KIT_API_VERSION')
accountkit_secret = getattr(settings, 'ACCOUNT_KIT_APP_SECRET')
accountkit_app_id = getattr(settings, 'ACCOUNT_KIT_APP_ID')
accountkit_success_redirect = getattr(settings, 'ACCOUNT_KIT_SUCCESS_REDIRECT', reverse('accountkit_success'))
accountkit_language_code = getattr(settings, 'ACCOUNT_KIT_LANGUAGE_CODE', 'en_US')


@register.simple_tag()
def accountkitheadjs():
    signer = TimestampSigner()
    state = signer.sign(accountkit_app_id)
    html = '''
<!-- HTTPS required. HTTP will give a 403 forbidden response -->
<script src="https://sdk.accountkit.com/{}/sdk.js"></script>
'''.format(accountkit_language_code)
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def accountkitbodyjs(context):
    signer = TimestampSigner()
    state = signer.sign(accountkit_app_id)
    request = context.get('request')
    redirect_url = request.build_absolute_uri(accountkit_success_redirect)
    html = '''
<script>
  // initialize Account Kit with CSRF protection
  AccountKit_OnInteractive = function(){{
    AccountKit.init(
      {{
        appId:"{}", 
        state:"{}", 
        version:"{}",
        fbAppEventsEnabled:true,
        redirect:"{}"
      }}
    );
  }};

  // login callback
  function loginCallback(response) {{
    if (response.status === "PARTIALLY_AUTHENTICATED") {{
      var code = response.code;
      var csrf = response.state;
      // Send code to server to exchange for access token
      var status=response.status;
      document.getElementById('code').value=code;
      document.getElementById('state').value=state;
      document.getElementById('status').value=status;
      document.getElementById('login').submit();
    }}
    else if (response.status === "NOT_AUTHENTICATED") {{
      // handle authentication failure
      var status=response.status;
      document.getElementById('status').value=status;
      document.getElementById('login').submit();
    }}
    else if (response.status === "BAD_PARAMS") {{
      // handle bad parameters
      var status=response.status;
      document.getElementById('status').value=status;
      document.getElementById('login').submit();
    }}
  }}

  // phone form submission handler
  function smsLogin() {{
    var countryCode = document.getElementById("country_code").value;
    var phoneNumber = document.getElementById("phone_number").value;
    AccountKit.login(
      'PHONE', 
      {{countryCode: countryCode, phoneNumber: phoneNumber}}, // will use default values if not specified
      loginCallback
    );
  }}

  // email form submission handler
  function emailLogin() {{
    var emailAddress = document.getElementById("email").value;
    AccountKit.login(
      'EMAIL',
      {{emailAddress: emailAddress}},
      loginCallback
    );
  }}
</script>
    '''.format(accountkit_app_id, state, accountkit_api_version, redirect_url)
    return mark_safe(html)
