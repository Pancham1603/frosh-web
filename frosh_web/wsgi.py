"""
WSGI config for frosh_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# import gevent.monkey
# gevent.monkey.patch_all()

# import gevent_psycopg2
# gevent_psycopg2.monkey_patch()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frosh_web.settings')

application = get_wsgi_application()
