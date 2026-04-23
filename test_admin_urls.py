import requests

# 测试 /admin/ 路径
response = requests.get('http://127.0.0.1:8000/admin/')
print(f"URL: /admin/")
print(f"Status code: {response.status_code}")
print(f"URL after redirect: {response.url}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response.headers.get('Content-Type')}")
print()

# 测试 /admin/login/ 路径
response = requests.get('http://127.0.0.1:8000/admin/login/')
print(f"URL: /admin/login/")
print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response.headers.get('Content-Type')}")
print()

# 测试 / 路径（数据大屏）
response = requests.get('http://127.0.0.1:8000/')
print(f"URL: /")
print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"Content type: {response.headers.get('Content-Type')}")