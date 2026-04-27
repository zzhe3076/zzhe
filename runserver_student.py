import os
import sys

os.chdir(r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'runserver', '8001', '--noreload'])
