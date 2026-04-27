import subprocess
import sys

script = """
import os
import django

os.chdir(r'd:\\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '8001', '--noreload'])
"""

proc = subprocess.Popen(
    [sys.executable, '-c', script],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=r'd:\xinshen'
)

print(f"Server started with PID: {proc.pid}")

import time
time.sleep(3)

if proc.poll() is None:
    print("Server is running!")
else:
    output = proc.stdout.read().decode('utf-8', errors='ignore')
    print(f"Server exited: {output}")
