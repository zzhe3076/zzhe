# 大学生新生报到智能助手

基于 Django + PostgreSQL 的高校新生报到管理系统。

## 功能

| 模块 | 状态 |
|:---|:---:|
| 学生管理 | ✅ |
| 报到登记 | ✅ |
| 数据统计 | ✅ |
| 学生端H5 | ✅ |
| Django Admin | ✅ |

## 技术栈

| 技术 | 版本 |
|:---|:---:|
| Django | 6.0.4 |
| DRF | - |
| PostgreSQL | 18 |
| Bootstrap | 5 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 迁移数据库
python manage.py migrate

# 创建管理员
python create_superuser.py

# 启动服务器
python manage.py runserver 8001
```

## 访问地址

| 功能 | 地址 |
|:---|:---|
| 数据大屏 | http://127.0.0.1:8001/ |
| 学生端 | http://127.0.0.1:8001/student/login/ |
| Admin | http://127.0.0.1:8001/admin/ |

**账号**: admin / admin123

---

**GitHub**: https://github.com/zzhe3076/zzhe
