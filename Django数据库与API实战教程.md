# Django 数据库与 API 实战教程

## —— 基于大学生新生报到系统

---

## 第一章：ORM 模型设计

### 1.1 模型类的定义

在 Django 中，每个模型类对应数据库中的一张表。请看 `models.py` 中的实际代码：

```python
# models.py 第5-19行
class College(models.Model):
    """学院模型"""
    name = models.CharField(max_length=100, verbose_name="学院名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="学院代码")
    description = models.TextField(blank=True, verbose_name="学院简介")
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时自动记录时间
    updated_at = models.DateTimeField(auto_now=True)     # 每次保存自动更新时间

    class Meta:
        db_table = "college"           # 指定数据库表名
        verbose_name = "学院"          # Admin后台显示名称
        verbose_name_plural = "学院"
        ordering = ['code']           # 默认排序

    def __str__(self):
        return self.name
```

**知识点**：
| 属性 | 说明 |
|:---|:---|
| `CharField` | 字符串字段，需指定 `max_length` |
| `TextField` | 长文本字段 |
| `DateTimeField` | 日期时间字段 |
| `auto_now_add=True` | 创建时自动设置 |
| `auto_now=True` | 每次更新时自动设置 |
| `unique=True` | 唯一约束 |
| `verbose_name` | Admin后台显示的中文名 |

---

### 1.2 字段类型一览

Django 提供的字段类型：

```python
# 常用字段类型
CharField(max_length=100)          # 字符串
TextField()                        # 长文本
IntegerField()                     # 整数
PositiveIntegerField()              # 正整数
DecimalField(max_digits=10, decimal_places=2)  # 小数
BooleanField()                     # 布尔值
DateField()                        # 日期
DateTimeField()                    # 日期时间
EmailField()                       # 邮箱
URLField()                         # 网址
ImageField(upload_to='photos/')    # 图片
FileField(upload_to='files/')     # 文件
JSONField()                        # JSON数据(PostgreSQL)
```

---

### 1.3 外键关系 (ForeignKey)

```python
# models.py 第22-37行
class Major(models.Model):
    """专业模型 - 属于某个学院"""
    name = models.CharField(max_length=100, verbose_name="专业名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="专业代码")
    
    # 外键：所属学院 (一对多关系)
    # on_delete=models.CASCADE - 删除学院时级联删除专业
    # related_name='majors' - 反向查询用 major.majors.all()
    college = models.ForeignKey(
        College, 
        on_delete=models.CASCADE, 
        related_name='majors', 
        verbose_name="所属学院"
    )
```

**关系示意图**：

```
College (学院)          Major (专业)
┌─────────────┐        ┌─────────────┐
│ id=1        │──────→│ college_id=1│
│ name=计算机  │        │ name=软件工程│
└─────────────┘        └─────────────┘
   1 ◄────────────────── N
```

---

### 1.4 完整的学生模型

```python
# models.py 第40-81行
class Student(models.Model):
    """学生模型 - 最核心的模型"""
    
    # ① 选择题字段
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    STATUS_CHOICES = [
        ('pending', '待报到'),
        ('checked_in', '已报到'),
        ('cancelled', '已取消'),
    ]
    
    # ② 一对一关系 (可选的用户账户)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        null=True, blank=True
    )
    
    # ③ 必填字段
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="性别")
    id_card = models.CharField(max_length=18, verbose_name="身份证号")
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    
    # ④ 外键关联
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='students')
    
    # ⑤ 可选字段
    class_name = models.CharField(max_length=50, blank=True)
    origin_province = models.CharField(max_length=50)
    origin_city = models.CharField(max_length=50, blank=True)
    high_school = models.CharField(max_length=100, blank=True)
    
    # ⑥ 状态字段 + 默认值
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'  # 默认待报到
    )
    
    # ⑦ 可为空的字段
    check_in_time = models.DateTimeField(null=True, blank=True)
    dynamic_code = models.CharField(max_length=32, unique=True, null=True, blank=True)
    dynamic_code_expires = models.DateTimeField(null=True, blank=True)
    
    # ⑧ 自动时间戳
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "student"
        # 索引：提升查询性能
        indexes = [
            models.Index(fields=['status', 'major']),           # 复合索引
            models.Index(fields=['origin_province']),         # 单列索引
        ]
    
    def __str__(self):
        return f"{self.student_id} - {self.name}"
```

---

### 1.5 模型关系总结

| 关系 | 代码 | 说明 |
|:---|:---|:---|
| 一对多 | `ForeignKey` | 1个学院→多个专业 |
| 一对一 | `OneToOneField` | 1个学生→1个用户账户 |
| 多对多 | `ManyToManyField` | (本项目未使用) |

---

## 第二章：序列化器 (Serializer)

### 2.1 什么是序列化器？

**序列化器的作用**：
- 模型对象 ↔ JSON 数据
- 输入验证
- 输出格式化

---

### 2.2 基本序列化器

```python
# serializers.py 第10-18行
class CollegeSerializer(serializers.ModelSerializer):
    """学院序列化器 - 最简单的形式"""
    
    # 计算字段：不存储在数据库中
    major_count = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = ['id', 'name', 'code', 'description', 'major_count', 'created_at', 'updated_at']

    def get_major_count(self, obj):
        """计算该学院的专业数量"""
        return obj.majors.count()
```

**知识点**：
- `ModelSerializer`：自动生成字段
- `SerializerMethodField`：自定义计算字段
- `source='field'`：指定数据来源

---

### 2.3 嵌套序列化器

```python
# serializers.py 第21-26行
class MajorSerializer(serializers.ModelSerializer):
    """专业序列化器 - 嵌套显示学院名称"""
    
    # 外键字段：自动显示关联对象的某个字段
    college_name = serializers.CharField(source='college.name', read_only=True)

    class Meta:
        model = Major
        fields = ['id', 'name', 'code', 'college', 'college_name', 'description', 'created_at', 'updated_at']
```

**`source` 语法**：
```python
source='college.name'    # 读取关联对象的属性
source='major.college.name'  # 多层嵌套
source='get_status_display'  # 调用方法获取Choices的显示值
```

---

### 2.4 学生序列化器 - 完整示例

```python
# serializers.py 第29-43行
class StudentSerializer(serializers.ModelSerializer):
    """学生序列化器 - 展示多种技巧"""
    
    # ① 嵌套读取：专业名称
    major_name = serializers.CharField(source='major.name', read_only=True)
    
    # ② 嵌套读取：学院名称 (两层嵌套)
    college_name = serializers.CharField(source='major.college.name', read_only=True)
    
    # ③ Choices显示值：状态的中文
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # ④ Choices显示值：性别的中文
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'name', 
            'gender', 'gender_display',   # 显示值
            'id_card', 'phone',
            'major', 'major_name',         # 嵌套
            'college_name',                # 两层嵌套
            'class_name', 'origin_province',
            'origin_city', 'high_school',
            'status', 'status_display',   # 显示值
            'check_in_time',
            'dynamic_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['dynamic_code', 'check_in_time']
```

---

### 2.5 创建时的序列化器

```python
# serializers.py 第46-72行
class StudentCreateSerializer(serializers.ModelSerializer):
    """创建学生时的序列化器 - 支持同时创建用户"""
    
    # 额外字段：不需要存储到Student表
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Student
        fields = [
            'username', 'password',  # 额外字段
            'student_id', 'name', 'gender', 'id_card',
            'phone', 'major', 'class_name', 
            'origin_province', 'origin_city', 'high_school'
        ]

    def create(self, validated_data):
        """创建时的自定义逻辑"""
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        
        # 如果没有提供username，使用student_id
        if not username:
            username = validated_data.get('student_id')
        
        # 同时创建User账户
        if username and password:
            user = User.objects.create_user(username=username, password=password)
        else:
            user = None
        
        # 创建Student记录
        student = Student.objects.create(user=user, **validated_data)
        return student
```

---

## 第三章：ViewSet 视图集

### 3.1 什么是 ViewSet？

ViewSet 是 Django REST Framework 提供的视图集，自动提供 CRUD 接口：

```python
# views.py 第23-28行
class CollegeViewSet(viewsets.ModelViewSet):
    """学院视图集 - 自动提供增删改查"""
    
    queryset = College.objects.all()           # 查询集
    serializer_class = CollegeSerializer      # 序列化器
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']          # 搜索字段
    ordering_fields = ['code', 'name']        # 可排序字段
```

**自动提供的接口**：

| 方法 | URL | 功能 |
|:---|:---|:---|
| GET | `/api/colleges/` | 列表 |
| POST | `/api/colleges/` | 创建 |
| GET | `/api/colleges/{id}/` | 详情 |
| PUT/PATCH | `/api/colleges/{id}/` | 更新 |
| DELETE | `/api/colleges/{id}/` | 删除 |

---

### 3.2 优化查询 - select_related

```python
# views.py 第31-36行
class MajorViewSet(viewsets.ModelViewSet):
    """专业视图集 - 优化查询"""
    
    # select_related: 预加载关联的学院对象 (SQL JOIN)
    # 避免 N+1 查询问题
    queryset = Major.objects.select_related('college').all()
    serializer_class = MajorSerializer
```

**优化对比**：

```python
# ❌ 慢: 每次访问 major.college 都会查询数据库
queryset = Major.objects.all()
for major in majors:
    print(major.college.name)  # N+1 查询!

# ✅ 快: 一次查询获取所有数据
queryset = Major.objects.select_related('college').all()
for major in majors:
    print(major.college.name)  # 无额外查询!
```

---

### 3.3 StudentViewSet - 完整示例

```python
# views.py 第46-98行
class StudentViewSet(viewsets.ModelViewSet):
    """学生视图集 - 完整功能"""
    
    # 预加载专业和学院，避免N+1
    queryset = Student.objects.select_related(
        'major', 'major__college', 'user'
    ).all()
    serializer_class = StudentSerializer
    
    # 搜索和排序
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'name', 'phone', 'id_card']
    ordering_fields = ['student_id', 'created_at']

    # ① 动态选择序列化器
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer  # 创建时用这个
        return StudentSerializer  # 其他操作用这个

    # ② 自定义过滤逻辑
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 获取URL参数
        status_param = self.request.query_params.get('status')
        major_id = self.request.query_params.get('major_id')
        college_id = self.request.query_params.get('college_id')
        origin_province = self.request.query_params.get('origin_province')

        # 条件过滤
        if status_param:
            queryset = queryset.filter(status=status_param)
        if major_id:
            queryset = queryset.filter(major_id=major_id)
        if college_id:
            queryset = queryset.filter(major__college_id=college_id)
        if origin_province:
            queryset = queryset.filter(origin_province=origin_province)

        return queryset

    # ③ 自定义动作：生成动态报到码
    @action(detail=True, methods=['post'])
    def generate_dynamic_code(self, request, pk=None):
        student = self.get_object()  # 获取当前学生
        if student.dynamic_code and student.dynamic_code_expires > timezone.now():
            return Response({
                'dynamic_code': student.dynamic_code,
                'expires_at': student.dynamic_code_expires
            })
        
        # 生成新的随机码
        student.dynamic_code = secrets.token_hex(16)
        student.dynamic_code_expires = timezone.now() + timedelta(minutes=30)
        student.save()
        
        return Response({
            'dynamic_code': student.dynamic_code,
            'expires_at': student.dynamic_code_expires
        })

    # ④ 自定义动作：获取所有省份
    @action(detail=False, methods=['get'])
    def provinces(self, request):
        provinces = Student.objects.values_list('origin_province', flat=True).distinct()
        return Response(list(provinces))
```

---

### 3.4 报到核心业务 - verify_and_checkin

```python
# views.py 第190-232行
class CheckInViewSet(viewsets.ModelViewSet):
    """报到视图集 - 核心业务逻辑"""
    
    queryset = CheckIn.objects.select_related('student', 'student__major').all()
    serializer_class = CheckInSerializer
    
    # 自定义动作：验证并报到
    @action(detail=False, methods=['post'])
    def verify_and_checkin(self, request):
        """验证学号和动态码，然后完成报到"""
        
        # ① 获取请求参数
        student_id = request.data.get('student_id')
        dynamic_code = request.data.get('dynamic_code', '')
        location = request.data.get('location', '线上报到')
        operator = request.data.get('operator', '系统')
        check_in_method = request.data.get('check_in_method', 'manual')
        remarks = request.data.get('remarks', '')

        # ② 验证学号是否存在
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response(
                {'error': '学号不存在'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # ③ 验证动态码（如果提供了的话）
        if dynamic_code:
            if student.dynamic_code != dynamic_code:
                return Response({'error': '核验码错误'}, status=status.HTTP_400_BAD_REQUEST)
            if student.dynamic_code_expires < timezone.now():
                return Response({'error': '核验码已过期，请重新生成'}, status=status.HTTP_400_BAD_REQUEST)

        # ④ 检查是否已报到
        if student.status == 'checked_in':
            return Response({'error': '已完成报到，无需重复操作'}, status=status.HTTP_400_BAD_REQUEST)

        # ⑤ 更新学生状态
        student.status = 'checked_in'
        student.check_in_time = timezone.now()
        student.dynamic_code = None
        student.dynamic_code_expires = None
        student.save()

        # ⑥ 创建报到记录
        check_in = CheckIn.objects.create(
            student=student,
            check_in_method=check_in_method,
            location=location,
            operator=operator,
            remarks=remarks
        )

        # ⑦ 返回结果
        return Response({
            'message': '报到成功',
            'check_in': CheckInSerializer(check_in).data,
            'student': StudentSerializer(student).data
        })
```

---

## 第四章：ORM 查询详解

### 4.1 基本查询

```python
# 查所有
students = Student.objects.all()

# 查单个（不存在会抛异常）
student = Student.objects.get(id=1)

# 查单个（安全，返回None）
student = Student.objects.filter(id=1).first()

# 条件查询
students = Student.objects.filter(status='pending')
students = Student.objects.exclude(status='cancelled')
```

### 4.2 链式查询

```python
# 链式调用：先过滤，再排序，再限制
students = (
    Student.objects
    .filter(status='pending')           # 过滤
    .filter(major__college_id=1)        # 外键过滤
    .order_by('-created_at')             # 排序
    [:10]                               # 取前10个
)
```

### 4.3 外键查询

```python
# 正向查询：学生 → 专业
student = Student.objects.get(id=1)
major = student.major  # 自动查询

# 反向查询：专业 → 学生
major = Major.objects.get(id=1)
students = major.students.all()  # related_name='students'

# 使用 filter 直接跨表查询
students = Student.objects.filter(major__college__name='计算机学院')
```

### 4.4 聚合查询

```python
from django.db.models import Count, Sum, Avg, Max, Min, Q

# 统计各状态学生数量
from django.db.models import Count
stats = Student.objects.values('status').annotate(count=Count('id'))

# 统计总数
total = Student.objects.count()

# 条件计数
pending_count = Student.objects.filter(status='pending').count()
```

### 4.5 Q 查询 - 复杂条件

```python
from django.db.models import Q

# OR 查询
students = Student.objects.filter(
    Q(status='pending') | Q(status='checked_in')
)

# NOT 查询
students = Student.objects.exclude(status='cancelled')

# 组合查询
students = Student.objects.filter(
    Q(status='pending') & Q(origin_province='北京')
)
```

---

## 第五章：路由配置

### 5.1 DRF 路由自动生成

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollegeViewSet, StudentViewSet, ...

# 创建路由器
router = DefaultRouter()

# 注册视图集 - 自动生成路由
router.register(r'colleges', CollegeViewSet)
router.register(r'students', StudentViewSet)
router.register(r'check-ins', CheckInViewSet)

# 包含到urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
```

### 5.2 生成的 URL

```
GET    /api/students/              # 列表
POST   /api/students/              # 创建
GET    /api/students/{id}/         # 详情
PUT    /api/students/{id}/         # 更新
DELETE /api/students/{id}/        # 删除
POST   /api/students/{id}/generate_dynamic_code/  # 自定义动作
GET    /api/students/provinces/    # 自定义动作
```

---

## 第六章：完整数据流示例

### 6.1 创建学生的完整流程

```
1. POST /api/students/
   │
   ▼
2. StudentCreateSerializer 验证数据
   │
   ▼
3. create() 方法创建 User 和 Student
   │
   ▼
4. 返回 StudentSerializer 序列化的JSON
```

```json
// 请求
POST /api/students/
{
    "student_id": "2024001",
    "name": "张三",
    "gender": "male",
    "id_card": "110101200001011234",
    "phone": "13800138001",
    "major": 1,
    "origin_province": "北京",
    "username": "zhangsan",
    "password": "123456"
}

// 响应
{
    "id": 1,
    "student_id": "2024001",
    "name": "张三",
    "gender": "male",
    "gender_display": "男",
    "major": 1,
    "major_name": "软件工程",
    "college_name": "计算机学院",
    "status": "pending",
    "status_display": "待报到",
    ...
}
```

### 6.2 报到流程

```
1. POST /api/check-ins/verify_and_checkin/
   │
   ▼
2. 验证学号存在
   │
   ▼
3. 验证动态码（可选）
   │
   ▼
4. 检查是否已报到
   │
   ▼
5. 更新 Student.status = 'checked_in'
   │
   ▼
6. 创建 CheckIn 记录
   │
   ▼
7. 返回报到结果
```

---

## 总结

| 知识点 | 代码位置 | 关键点 |
|:---|:---|:---|
| 模型定义 | models.py | CharField, ForeignKey, Meta配置 |
| 序列化器 | serializers.py | ModelSerializer, source, SerializerMethodField |
| 视图集 | views.py | ModelViewSet, select_related, 自定义action |
| 路由 | urls.py | DefaultRouter, register |
| ORM查询 | views.py | filter, select_related, annotate |

---

**文档版本**: V1.0
**基于项目**: 大学生新生报到智能助手
**编制日期**: 2026-04-27
