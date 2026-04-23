import os
import sys
import django

sys.path.insert(0, r'd:\xinshen')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcome_assistant.settings')
django.setup()

from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT version()')
version = cursor.fetchone()
print('Database connected!')
print('PostgreSQL version:', version[0])
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
