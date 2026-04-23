cd d:\xinshen
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT version()')
version = cursor.fetchone()
print('Database connected!')
print('PostgreSQL version:', version[0])
cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public'\")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
"
