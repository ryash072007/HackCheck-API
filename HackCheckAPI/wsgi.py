"""
WSGI config for HackCheckAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# from django.core.management import call_command


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackCheckAPI.settings')

application = get_wsgi_application()

# print(f"{os.path.join('/tmp', 'db.sqlite3')}, {os.path.exists(os.path.join('/tmp', 'db.sqlite3'))}")
# # Apply all migrations
# call_command("migrate")

# print(f"{os.path.join('/tmp', 'db.sqlite3')}, {os.path.exists(os.path.join('/tmp', 'db.sqlite3'))}")