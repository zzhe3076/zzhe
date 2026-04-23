from django.db import models
from django.contrib.auth.models import User


class College(models.Model):
    name = models.CharField(max_length=100, verbose_name="学院名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="学院代码")
    description = models.TextField(blank=True, verbose_name="学院简介")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "college"
        verbose_name = "学院"
        verbose_name_plural = "学院"
        ordering = ['code']

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=100, verbose_name="专业名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="专业代码")
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='majors', verbose_name="所属学院")
    description = models.TextField(blank=True, verbose_name="专业简介")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "major"
        verbose_name = "专业"
        verbose_name_plural = "专业"
        ordering = ['code']

    def __str__(self):
        return f"{self.college.name} - {self.name}"


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    STATUS_CHOICES = [
        ('pending', '待报到'),
        ('checked_in', '已报到'),
        ('cancelled', '已取消'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', verbose_name="用户", null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="性别")
    id_card = models.CharField(max_length=18, verbose_name="身份证号")
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='students', verbose_name="专业")
    class_name = models.CharField(max_length=50, blank=True, verbose_name="班级")
    origin_province = models.CharField(max_length=50, verbose_name="生源省份")
    origin_city = models.CharField(max_length=50, blank=True, verbose_name="生源城市")
    high_school = models.CharField(max_length=100, blank=True, verbose_name="毕业高中")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="报到状态")
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name="报到时间")
    dynamic_code = models.CharField(max_length=32, unique=True, null=True, blank=True, verbose_name="动态核验码")
    dynamic_code_expires = models.DateTimeField(null=True, blank=True, verbose_name="核验码过期时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student"
        verbose_name = "学生"
        verbose_name_plural = "学生"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'major']),
            models.Index(fields=['origin_province']),
        ]

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class DormitoryBuilding(models.Model):
    name = models.CharField(max_length=100, verbose_name="楼栋名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="楼栋代码")
    floor_count = models.PositiveIntegerField(verbose_name="楼层数")
    total_rooms = models.PositiveIntegerField(verbose_name="总房间数")
    available_rooms = models.PositiveIntegerField(verbose_name="可用房间数")
    gender_restriction = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女'), ('mixed', '混合')], default='mixed', verbose_name="性别限制")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dormitory_building"
        verbose_name = "宿舍楼栋"
        verbose_name_plural = "宿舍楼栋"
        ordering = ['code']

    def __str__(self):
        return self.name


class DormitoryRoom(models.Model):
    building = models.ForeignKey(DormitoryBuilding, on_delete=models.CASCADE, related_name='rooms', verbose_name="楼栋")
    room_number = models.CharField(max_length=20, verbose_name="房间号")
    floor = models.PositiveIntegerField(verbose_name="楼层")
    capacity = models.PositiveIntegerField(default=4, verbose_name="床位容量")
    current_occupancy = models.PositiveIntegerField(default=0, verbose_name="当前入住人数")
    room_type = models.CharField(max_length=50, choices=[('standard', '标准间'), ('upgrade', '升级间')], default='standard', verbose_name="房间类型")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="住宿费")
    is_available = models.BooleanField(default=True, verbose_name="是否可用")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dormitory_room"
        verbose_name = "宿舍房间"
        verbose_name_plural = "宿舍房间"
        ordering = ['building', 'room_number']
        unique_together = ['building', 'room_number']

    def __str__(self):
        return f"{self.building.name} - {self.room_number}"


class DormitoryAssignment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dormitory_assignment', verbose_name="学生")
    room = models.ForeignKey(DormitoryRoom, on_delete=models.CASCADE, related_name='assignments', verbose_name="分配房间")
    bed_number = models.PositiveIntegerField(verbose_name="床位号")
    assignment_date = models.DateTimeField(auto_now_add=True, verbose_name="分配时间")
    status = models.CharField(max_length=20, choices=[('assigned', '已分配'), ('checked_in', '已入住'), ('cancelled', '已取消')], default='assigned', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dormitory_assignment"
        verbose_name = "宿舍分配"
        verbose_name_plural = "宿舍分配"

    def __str__(self):
        return f"{self.student.name} - {self.room}"


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('tuition', '学费'),
        ('accommodation', '住宿费'),
        ('material', '教材费'),
        ('other', '其他'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name="学生")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name="缴费类型")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="缴费状态")
    order_number = models.CharField(max_length=50, unique=True, verbose_name="订单号")
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="支付方式")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="交易流水号")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment"
        verbose_name = "缴费记录"
        verbose_name_plural = "缴费记录"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.payment_type} - {self.amount}"


class CheckIn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='check_in_records', verbose_name="学生")
    check_in_method = models.CharField(max_length=20, choices=[('manual', '人工核验'), ('qrcode', '扫码核验')], verbose_name="报到方式")
    location = models.CharField(max_length=100, verbose_name="报到地点")
    operator = models.CharField(max_length=50, verbose_name="操作人")
    remarks = models.TextField(blank=True, verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="报到时间")

    class Meta:
        db_table = "check_in"
        verbose_name = "报到记录"
        verbose_name_plural = "报到记录"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class KnowledgeBase(models.Model):
    CATEGORY_CHOICES = [
        ('admission', '报到流程'),
        ('payment', '缴费标准'),
        ('dormitory', '宿舍分配'),
        ('facility', '设施使用'),
        ('transportation', '交通指南'),
        ('other', '其他'),
    ]

    question = models.TextField(verbose_name="问题")
    answer = models.TextField(verbose_name="答案")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="分类")
    keywords = models.CharField(max_length=500, blank=True, verbose_name="关键词(逗号分隔)")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    view_count = models.PositiveIntegerField(default=0, verbose_name="查看次数")
    helpful_count = models.PositiveIntegerField(default=0, verbose_name="有帮助次数")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "knowledge_base"
        verbose_name = "知识库"
        verbose_name_plural = "知识库"
        ordering = ['-view_count']
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.question[:50]


class FAQ(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='faqs', verbose_name="提问学生", null=True, blank=True)
    question = models.TextField(verbose_name="问题")
    answer = models.TextField(verbose_name="答案", blank=True)
    is_answered = models.BooleanField(default=False, verbose_name="是否已回答")
    is_published = models.BooleanField(default=False, verbose_name="是否公开")
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True, verbose_name="回答时间")

    class Meta:
        db_table = "faq"
        verbose_name = "常见问题"
        verbose_name_plural = "常见问题"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    priority = models.CharField(max_length=20, choices=[('high', '高'), ('normal', '普通'), ('low', '低')], default='normal', verbose_name="优先级")
    target_audience = models.CharField(max_length=50, choices=[('all', '全体'), ('college', '按学院'), ('major', '按专业')], default='all', verbose_name="目标受众")
    target_college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='announcements', verbose_name="目标学院")
    target_major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True, blank=True, related_name='announcements', verbose_name="目标专业")
    is_published = models.BooleanField(default=False, verbose_name="是否发布")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="发布时间")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "announcement"
        verbose_name = "公告"
        verbose_name_plural = "公告"
        ordering = ['-priority', '-published_at']

    def __str__(self):
        return self.title


class SystemConfig(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name="配置键")
    value = models.TextField(verbose_name="配置值")
    description = models.CharField(max_length=200, blank=True, verbose_name="说明")
    is_public = models.BooleanField(default=False, verbose_name="是否公开")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "system_config"
        verbose_name = "系统配置"
        verbose_name_plural = "系统配置"

    def __str__(self):
        return self.key
