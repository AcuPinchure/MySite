"""
WSGI config for MySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys

#if Use ENVh
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
sys.path.append('/root/Documents/MySite/venv')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MySite.settings')

application = get_wsgi_application()
