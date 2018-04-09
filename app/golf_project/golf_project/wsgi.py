"""
WSGI config for golf_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "golf_project.settings")

from django.core.wsgi import get_wsgi_application
from django.whitenoise import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
