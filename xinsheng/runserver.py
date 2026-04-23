import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])
