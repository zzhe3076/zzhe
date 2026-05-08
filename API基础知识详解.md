# API基础知识详解

## —— 基于大学生新生报到系统

---

## 第一章：API基本概念

### 1.1 什么是API？

**API = 应用程序编程接口**

简单说：API就是"数据的中转站"

```
传统网页:                       API方式:
┌─────────┐                   ┌─────────┐
│ 用户浏览器│   请求整个页面    │ 用户    │   请求数据
│         │ ◄─────────────────│        │ ◄──────────
│ 返回HTML│                   │ 返回JSON│
└─────────┘                   └─────────┘
```

### 1.2 为什么用API？

| 优点 | 说明 |
|:---|:---|
| 前后端分离 | 前端和后端可以独立开发 |
| 跨平台 | 一个API，多个客户端（网页/APP/小程序） |
| 效率高 | 只传数据，不传页面 |
| 易于集成 | 其他系统可以调用 |

---

## 第二章：HTTP协议基础

### 2.1 什么是HTTP？

**HTTP = 超文本传输协议**

浏览器和服务器之间的"对话语言"

```
浏览器 ──请求──► 服务器
浏览器 ◄──响应── 服务器

请求格式:
┌─────────────────────────────────┐
│ GET /api/students HTTP/1.1     │  ← 请求行
│ Host: localhost:8001           │  ← 请求头
│ Content-Type: application/json │
│                                 │
│ {                              │  ← 请求体
│   "name": "张三"               │
│ }                              │
└─────────────────────────────────┘
```

### 2.2 请求方法

| 方法 | 含义 | 例子 |
|:---|:---|:---|
| GET | 获取数据 | 查资料 |
| POST | 创建数据 | 提交表单 |
| PUT | 完整更新 | 全部替换 |
| PATCH | 部分更新 | 只改一部分 |
| DELETE | 删除数据 | 删除记录 |

**记忆口诀**：
- GET = 看（获取）
- POST = 增（创建）
- PUT = 改（完整）
- PATCH = 改（部分）
- DELETE = 删

### 2.3 状态码

| 状态码 | 含义 | 例子 |
|:---|:---|:---|
| 200 | 成功 | OK |
| 201 | 创建成功 | Created |
| 400 | 请求错误 | Bad Request |
| 401 | 未授权 | Unauthorized |
| 403 | 禁止访问 | Forbidden |
| 404 | 找不到 | Not Found |
| 500 | 服务器错误 | Server Error |

---

## 第三章：RESTful API

### 3.1 什么是RESTful？

**RESTful = 一种API设计规范**

```
URL设计规范:
┌─────────────────────────────────────┐
│  不使用:            │  使用:        │
│  /getStudents      │  GET /students│
│  /createStudent   │  POST /students│
│  /deleteStudent   │  DELETE /students/1│
│  /updateStudent   │  PUT /students/1 │
└─────────────────────────────────────┘
```

### 3.2 RESTful URL设计

```
# 资源命名: 用名词，不用动词

GET    /students          # 获取学生列表
POST   /students          # 创建学生
GET    /students/1       # 获取id=1的学生
PUT    /students/1       # 更新id=1的学生
DELETE /students/1       # 删除id=1的学生

# 特殊操作
POST   /students/1/checkin  # 让学生报到(动作)
GET    /students/provinces   # 获取所有省份(获取列表)
```

### 3.3 RESTful 响应格式

```json
// 成功响应
{
    "success": true,
    "data": {
        "id": 1,
        "name": "张三",
        "status": "pending"
    }
}

// 列表响应
{
    "count": 100,
    "next": "http://localhost:8001/api/students?page=2",
    "previous": null,
    "results": [
        {"id": 1, "name": "张三"},
        {"id": 2, "name": "李四"}
    ]
}

// 错误响应
{
    "success": false,
    "error": "学号不存在",
    "code": 400
}
```

---

## 第四章：JSON数据格式

### 4.1 什么是JSON？

**JSON = JavaScript对象表示法**

现在最流行的数据交换格式

```json
// JSON 例子
{
    "name": "张三",
    "age": 20,
    "isStudent": true,
    "courses": ["语文", "数学", "英语"],
    "address": {
        "city": "北京",
        "district": "朝阳区"
    }
}
```

### 4.2 JSON 数据类型

| 类型 | 示例 |
|:---|:---|
| 字符串 | "Hello" |
| 数字 | 20, 3.14 |
| 布尔 | true, false |
| 空值 | null |
| 数组 | [1, 2, 3] |
| 对象 | {"key": "value"} |

---

## 第五章：Django REST Framework

### 5.1 什么是DRF？

**Django REST Framework = Django的API开发工具**

```
不用DRF:                      用DRF:
┌─────────────┐               ┌─────────────┐
│ 写大量代码   │    →        │ 几行代码    │
│ 处理JSON    │               │ 自动处理    │
│ 手动写验证  │               │ 内置验证    │
└─────────────┘               └─────────────┘
```

### 5.2 DRF 核心组件

| 组件 | 作用 |
|:---|:---|
| Serializer | 模型 ↔ JSON 转换 |
| ViewSet | 提供API接口 |
| Router | 自动生成URL |
| Authentication | 用户认证 |
| Permission | 权限控制 |
| Pagination | 分页 |
| Filtering | 过滤 |

### 5.3 安装DRF

```bash
pip install djangorestframework
```

在 settings.py 中添加：

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## 第六章：Serializer 序列化器

### 6.1 什么是序列化器？

**作用：模型对象 ↔ JSON**

```python
# serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'student_id', 'status']
```

### 6.2 序列化（模型→JSON）

```python
# 序列化单个对象
student = Student.objects.get(id=1)
serializer = StudentSerializer(student)
print(serializer.data)
# 输出: {'id': 1, 'name': '张三', 'student_id': '001', 'status': 'pending'}

# 序列化多个对象
students = Student.objects.all()
serializer = StudentSerializer(students, many=True)
print(serializer.data)
```

### 6.3 反序列化（JSON→模型）

```python
# 验证数据
data = {'name': '李四', 'student_id': '002'}
serializer = StudentSerializer(data=data)
serializer.is_valid()  # 验证是否有效
# 输出: True

# 保存数据
serializer.save()
```

### 6.4 自定义字段

```python
class StudentSerializer(serializers.ModelSerializer):
    # 1. 嵌套显示
    major_name = serializers.CharField(source='major.name', read_only=True)
    
    # 2. 计算字段
    status_text = serializers.SerializerMethodField()
    def get_status_text(self, obj):
        return "已报到" if obj.status == 'checked_in' else "待报到"

    # 3. Choices显示值
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'major_name', 'status', 'status_text', 'status_display']
```

---

## 第七章：ViewSet 视图集

### 7.1 什么是ViewSet？

**ViewSet = 快速创建API的视图**

```python
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

**自动提供的接口**：

| 方法 | URL | 功能 |
|:---|:---|:---|
| GET | /students/ | 列表 |
| POST | /students/ | 创建 |
| GET | /students/1/ | 详情 |
| PUT | /students/1/ | 完整更新 |
| PATCH | /students/1/ | 部分更新 |
| DELETE | /students/1/ | 删除 |

### 7.2 自定义查询

```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    # 自定义过滤
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 获取URL参数
        status = self.request.query_params.get('status')
        
        # 过滤
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
```

### 7.3 自定义动作

```python
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    # 自定义API: 生成报到码
    @action(detail=True, methods=['post'])
    def generate_code(self, request, pk=None):
        student = self.get_object()  # 获取当前学生
        
        # 生成随机码
        import secrets
        code = secrets.token_hex(16)
        student.dynamic_code = code
        student.save()
        
        return Response({'code': code, 'message': '生成成功'})
```

---

## 第八章：路由配置

### 8.1 自动路由

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

# 创建路由器
router = DefaultRouter()

# 注册视图集
router.register(r'students', StudentViewSet)

# 添加到urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
```

### 8.2 生成的URL

```
GET    /api/students/                  # 列表
POST   /api/students/                  # 创建
GET    /api/students/1/                # 详情
PUT    /api/students/1/                # 更新
DELETE /api/students/1/                # 删除
POST   /api/students/1/generate_code/  # 自定义动作
```

---

## 第九章：认证与权限

### 9.1 认证方式

| 方式 | 说明 |
|:---|:---|
| Session | Cookie认证 |
| Token | Token认证 |
| JWT | JSON Web Token |
| OAuth | 第三方登录 |

### 9.2 DRF 认证配置

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 9.3 自定义权限

```python
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
```

---

## 第十章：分页与过滤

### 10.1 分页

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### 10.2 过滤

```python
# views.py
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'student_id']  # 搜索字段
    ordering_fields = ['created_at', 'name']  # 排序字段
```

**使用**：
```
GET /api/students/?search=张       # 搜索"张"
GET /api/students/?ordering=-created_at  # 按时间降序
GET /api/students/?status=pending  # 过滤状态
```

---

## 第十一章：本项目API详解

### 11.1 学生管理API

```http
GET /api/students/
```
**响应**:
```json
{
    "count": 100,
    "results": [
        {
            "id": 1,
            "name": "张三",
            "student_id": "2024001",
            "status": "pending",
            "major_name": "软件工程"
        }
    ]
}
```

```http
POST /api/students/
```
**请求**:
```json
{
    "name": "李四",
    "student_id": "2024002",
    "phone": "13800138002",
    "major": 1,
    "gender": "male"
}
```

### 11.2 报到API

```http
POST /api/check-ins/verify_and_checkin/
```
**请求**:
```json
{
    "student_id": "2024001",
    "check_in_method": "manual",
    "location": "报到处A",
    "operator": "管理员"
}
```
**响应**:
```json
{
    "message": "报到成功",
    "student": {
        "id": 1,
        "name": "张三",
        "status": "checked_in"
    }
}
```

### 11.3 统计API

```http
GET /api/dashboard/stats/
```
**响应**:
```json
{
    "total_students": 100,
    "checked_in": 45,
    "pending": 55,
    "check_in_rate": 45.0,
    "today_checked_in": 10
}
```

---

## 第十二章：API调用示例

### 12.1 使用curl

```bash
# GET 请求
curl http://127.0.0.1:8001/api/students/

# POST 请求
curl -X POST http://127.0.0.1:8001/api/students/ \
     -H "Content-Type: application/json" \
     -d '{"name":"张三","student_id":"001"}'
```

### 12.2 使用Python requests

```python
import requests

# GET 请求
response = requests.get('http://127.0.0.1:8001/api/students/')
students = response.json()
print(students)

# POST 请求
data = {
    'name': '张三',
    'student_id': '001',
    'phone': '13800138001',
    'major': 1
}
response = requests.post(
    'http://127.0.0.1:8001/api/students/',
    json=data
)
print(response.status_code)
```

### 12.3 前端JavaScript调用

```javascript
// GET 请求
fetch('http://127.0.0.1:8001/api/students/')
    .then(res => res.json())
    .then(data => console.log(data));

// POST 请求
fetch('http://127.0.0.1:8001/api/students/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        name: '张三',
        student_id: '001'
    })
})
    .then(res => res.json())
    .then(data => console.log(data));
```

---

## 第十三章：常见问题

### 13.1 跨域问题（CORS）

浏览器默认禁止AJAX请求其他域名

**解决**：安装django-cors-headers

```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
```

### 13.2 如何选择API框架？

| 框架 | 适用场景 |
|:---|:---|
| Django REST Framework | Django项目 |
| FastAPI | Python高性能API |
| Flask | 轻量级API |
| Express.js | Node.js API |
| Spring Boot | Java API |

---

## 总结

| 知识点 | 核心内容 |
|:---|:---|
| HTTP | 请求方法、状态码 |
| RESTful | URL设计规范 |
| JSON | 数据格式 |
| DRF | Django API开发工具 |
| Serializer | 模型↔JSON转换 |
| ViewSet | 快速创建API |
| 认证 | Session/Token/JWT |
| 过滤分页 | 查询优化 |

---

**版本**: V1.0
**编制日期**: 2026-04-27
