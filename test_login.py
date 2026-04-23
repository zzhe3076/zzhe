import requests
r = requests.get('http://127.0.0.1:8000/admin/login/')
print('Status:', r.status_code)
print('URL:', r.url)
print('Content length:', len(r.text))
print('First 500 chars:', r.text[:500])