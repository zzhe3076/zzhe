cd d:\xinshen
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created!')
    print('Username: admin')
    print('Password: admin123')
else:
    user = User.objects.get(username='admin')
    print('Superuser already exists!')
    print('Username:', user.username)
"
