from django.conf import settings

def settings_context(request):
    return {
        'settings': {
            'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        }
    }