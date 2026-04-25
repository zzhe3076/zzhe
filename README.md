# 大学生新生报到智能助手

[![Django](https://img.shields.io/badge/Django-6.0.4-brightgreen)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com/)

基于 Django + PostgreSQL 的大学新生报到管理系统，为高校提供新生报到、宿舍分配、缴费管理、数据统计等功能。

## 功能特性

### ✅ 已完成功能

| 模块 | 功能 |
|:---|:---|
| 学生管理 | 学生信息录入、编辑、删除、搜索、报到状态管理 |
| 报到管理 | 人工报到登记、动态核验码生成、报到记录查询 |
| 数据统计 | 实时报到数据大屏、各学院统计、生源地统计 |
| Django管理后台 | 全模型CRUD管理 |

### ⚠️ 待完善功能

| 模块 | 说明 |
|:---|:---|
| 宿舍管理 | 需填充数据 |
| 缴费管理 | 需填充数据 |
| 公告通知 | 需填充数据 |
| 知识库/FAQ | 需填充数据 |
| 微信小程序 | 需配置AppID |

## 技术栈

| 技术 | 版本 |
|:---|:---|
| 后端框架 | Django 6.0.4 |
| API框架 | Django REST Framework |
| 数据库 | PostgreSQL 18 |
| 前端 | Bootstrap 5 + JavaScript |
| 小程序 | 微信小程序 |

## 项目结构

```
xinshen/
├── welcome_app/               # 主应用
│   ├── models.py             # 数据模型
│   ├── views.py              # REST API视图
│   ├── wechat_views.py       # 微信小程序API
│   ├── serializers.py        # API序列化
│   ├── urls.py               # REST路由
│   ├── wechat_urls.py        # 微信API路由
│   ├── frontend_urls.py      # 前端页面路由
│   └── frontend_views.py     # 前端视图
├── welcome_assistant/        # 项目配置
│   ├── settings.py           # Django配置
│   └── urls.py               # 主路由
├── templates/                # HTML模板
│   ├── base.html
│   └── frontend/             # 前端页面
│       ├── index.html        # 数据大屏
│       ├── checkin.html      # 扫码报到
│       └── students.html     # 学生管理
├── wechat小程序/             # 微信小程序代码
├── manage.py
├── requirements.txt
└── MVP技术方案.md            # 技术方案文档
```

## 快速开始

### 环境要求

- Python 3.8+
- PostgreSQL 18
- Windows / Linux / macOS

### 1. 克隆项目

```bash
git clone https://github.com/zzhe3076/zzhe.git
cd zzhe
```

### 2. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

确保 PostgreSQL 已启动，并创建数据库：

```sql
CREATE DATABASE welcome_assistant;
```

配置数据库连接（可选，默认已配置）：

```python
# welcome_assistant/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'welcome_assistant',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. 配置 PostgreSQL 认证

编辑 `pg_hba.conf` 文件，将认证方式改为 `trust`：

```conf
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
```

重启 PostgreSQL：
```bash
pg_ctl reload
```

### 6. 迁移数据库

```bash
python manage.py migrate
```

### 7. 创建超级管理员

```bash
python manage.py createsuperuser
# 或使用脚本
python create_superuser.py
```

### 8. 启动服务器

```bash
python manage.py runserver 8001
```

## 访问地址

| 功能 | 地址 |
|:---|:---|
| 数据大屏 | http://127.0.0.1:8001/ |
| 扫码报到 | http://127.0.0.1:8001/checkin/ |
| 学生管理 | http://127.0.0.1:8001/students/ |
| Django管理后台 | http://127.0.0.1:8001/admin/ |

默认管理员账号：`admin` / `admin123`

## API 接口

### REST API

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/colleges/` | GET/POST | 学院管理 |
| `/api/majors/` | GET/POST | 专业管理 |
| `/api/students/` | GET/POST | 学生管理 |
| `/api/check-ins/` | GET/POST | 报到记录 |
| `/api/check-ins/verify_and_checkin/` | POST | 验证并报到 |
| `/api/dashboard/stats/` | GET | 数据统计 |

### 微信小程序 API

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/wechat/login/` | POST | 微信登录 |
| `/api/wechat/bind/` | POST | 绑定学生 |
| `/api/wechat/dashboard/` | GET | 个人中心 |
| `/api/wechat/generate_code/` | POST | 生成报到码 |
| `/api/wechat/verify_checkin/` | POST | 扫码报到 |

> ⚠️ 微信小程序接口需要配置 AppID 和 Secret 才能使用

## 数据库表

| 表名 | 说明 | 状态 |
|:---|:---|:---:|
| college | 学院表 | ✅ 有数据 |
| major | 专业表 | ✅ 有数据 |
| student | 学生表 | ✅ 有数据 |
| check_in | 报到记录表 | ✅ 有数据 |
| dormitory_building | 宿舍楼栋表 | ❌ 暂无数据 |
| dormitory_room | 宿舍房间表 | ❌ 暂无数据 |
| dormitory_assignment | 宿舍分配表 | ❌ 暂无数据 |
| payment | 缴费记录表 | ❌ 暂无数据 |
| knowledge_base | 知识库表 | ❌ 暂无数据 |
| faq | 常见问题表 | ❌ 暂无数据 |
| announcement | 公告表 | ❌ 暂无数据 |
| system_config | 系统配置表 | ❌ 暂无数据 |

## 开发计划

| 阶段 | 任务 |
|:---:|:---|
| Week 1-4 | ✅ 核心功能开发（已完成） |
| Week 5 | 数据填充（宿舍、缴费、公告、FAQ） |
| Week 6 | 微信小程序配置 |
| Week 7 | 部署上线 |

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**项目作者**: 丁元  
**技术栈**: Django + PostgreSQL + Bootstrap + 微信小程序  
**项目地址**: https://github.com/zzhe3076/zzhe
