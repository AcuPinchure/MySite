"""
WSGI config for MySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys

project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_home not in sys.path:
    # print(project_home)
    sys.path.append(project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MySite.settings')

application = get_wsgi_application()
