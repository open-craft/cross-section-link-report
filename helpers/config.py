from django.conf import settings

LMS_URL = settings.LMS_ROOT_URL
STUDIO_URL = f"http{'s' if settings.HTTPS == 'on' else ''}://{settings.CMS_BASE}"

INSTANCE_NAME = settings.SITE_NAME
