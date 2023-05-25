from django.conf import settings

HTTPS = settings.HTTPS == 'on'
LMS_BASE_URL = settings.LMS_BASE
LMS_URL = settings.LMS_ROOT_URL
STUDIO_URL = f"http{'s' if HTTPS else ''}://{settings.CMS_BASE}"

INSTANCE_NAME = settings.SITE_NAME
