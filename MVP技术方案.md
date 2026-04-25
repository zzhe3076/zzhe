# 大学生新生报到智能助手 - 技术方案文档 V2.0

## 文档信息

| 项目 | 内容 |
|:---|:---|
| 版本 | V2.0 |
| 日期 | 2026-04-23 |
| 状态 | MVP已完成 |
| 作者 | 丁元 |

---

## 一、项目概述

### 1.1 项目背景

随着高校信息化建设的发展，传统的新生报到方式存在效率低、数据统计困难等问题。本项目旨在构建一个高效的数字化新生报到管理系统，实现报到流程的自动化和数据的实时统计。

### 1.2 项目目标

1. **提高报到效率** - 减少人工操作，缩短新生等待时间
2. **数据实时统计** - 实时掌握报到进度，支持多维度统计分析
3. **移动端支持** - 支持微信小程序，方便学生随时查看状态
4. **系统化管理** - 统一管理学生信息、宿舍分配、缴费等数据

### 1.3 核心价值主张

> 让新生一部手机完成报到，让校方实时掌握报到进度

---

## 二、系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            用户接入层                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐ │
│  │   微信小程序     │  │   Web管理端      │  │   Django Admin          │ │
│  │   (待配置)      │  │   ✅ 已完成     │  │   ✅ 已完成            │ │
│  └────────┬────────┘  └────────┬────────┘  └───────────┬─────────────┘ │
│           │                    │                       │                │
│           └────────────────────┼───────────────────────┘                │
│                                ▼                                        │
│                    ┌─────────────────────┐                             │
│                    │     Nginx 网关       │  负载均衡/静态资源          │
│                    │    (生产环境部署)    │                             │
│                    └──────────┬──────────┘                             │
│                               ▼                                        │
│                    ┌─────────────────────┐                             │
│                    │   Django API 层     │  REST API + 业务逻辑        │
│                    │   ✅ 已完成        │                             │
│                    └──────────┬──────────┘                             │
│                               ▼                                        │
│                    ┌─────────────────────┐                             │
│                    │   PostgreSQL 18     │  数据持久化                 │
│                    │   ✅ 已配置        │                             │
│                    └─────────────────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 技术选型

| 层级 | 技术方案 | 版本 | 状态 |
|:---|:---|:---:|:---:|
| 前端（管理端） | Bootstrap | 5.3 | ✅ 已完成 |
| 前端（小程序） | 微信小程序原生 | - | ⚠️ 待配置 |
| 后端框架 | Django | 6.0.4 | ✅ 已完成 |
| API框架 | Django REST Framework | 3.14 | ✅ 已完成 |
| 数据库 | PostgreSQL | 18 | ✅ 已完成 |
| 认证方式 | Django Session | - | ✅ 已完成 |
| Web服务器 | Django Dev Server | - | ✅ 运行中 |

### 2.3 目录结构

```
xinshen/
├── welcome_app/                      # 主应用
│   ├── models.py                     # 12个数据模型
│   ├── views.py                      # REST API视图
│   ├── wechat_views.py               # 微信小程序API
│   ├── serializers.py                # API序列化器
│   ├── urls.py                       # REST路由配置
│   ├── wechat_urls.py                # 微信API路由
│   ├── frontend_urls.py              # 前端页面路由
│   ├── frontend_views.py             # 前端视图
│   ├── admin.py                     # Django Admin配置
│   ├── middleware.py                # 中间件
│   ├── exceptions.py                # 自定义异常
│   ├── tests.py                     # 测试用例
│   └── migrations/                  # 数据库迁移
│       ├── 0001_initial.py
│       └── 0002_alter_student_user.py
├── welcome_assistant/               # 项目配置
│   ├── settings.py                  # Django设置
│   ├── urls.py                      # 主路由配置
│   ├── wsgi.py                     # WSGI配置
│   └── asgi.py                     # ASGI配置
├── templates/                       # HTML模板
│   ├── base.html                    # 基础模板
│   └── frontend/                    # 前端页面
│       ├── index.html               # 数据大屏
│       ├── checkin.html             # 扫码报到
│       └── students.html            # 学生管理
├── wechat小程序/                    # 微信小程序源码
│   └── miniprogram/
│       ├── app.js
│       ├── app.json
│       └── pages/                   # 页面目录
│           ├── index/               # 首页
│           ├── login/               # 登录
│           ├── bind/                # 绑定
│           ├── dashboard/           # 个人中心
│           ├── qrcode/              # 报到码
│           ├── payment/             # 缴费
│           ├── dormitory/           # 宿舍
│           ├── announcement/        # 公告
│           └── faq/                # 问答
├── deploy/                          # 部署配置
│   └── nginx.conf                   # Nginx配置
├── logs/                           # 日志目录
├── media/                          # 媒体文件
├── staticfiles/                    # 静态文件
├── manage.py                       # Django管理脚本
├── requirements.txt                 # Python依赖
├── Dockerfile                      # Docker配置
├── MVP技术方案.md                   # MVP技术方案
├── 功能实现总结.md                  # 功能实现总结
└── README.md                       # 项目说明文档
```

---

## 三、功能模块

### 3.1 已完成功能模块

#### 3.1.1 学生管理模块 ✅

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 学生信息录入 | 新增学生基本信息 | ✅ |
| 学生信息编辑 | 修改学生信息 | ✅ |
| 学生信息删除 | 删除学生记录 | ✅ |
| 学号唯一性校验 | 自动检查学号重复 | ✅ |
| 按状态筛选 | 待报到/已报到/已取消 | ✅ |
| 按学院筛选 | 按学院筛选学生 | ✅ |
| 按专业筛选 | 按专业筛选学生 | ✅ |
| 搜索功能 | 按姓名/学号/电话搜索 | ✅ |

#### 3.1.2 报到管理模块 ✅

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 人工报到 | 手动输入学号完成报到 | ✅ |
| 动态核验码 | 生成30分钟有效期核验码 | ✅ |
| 核验码验证 | 验证核验码有效性 | ✅ |
| 报到记录 | 记录报到时间、地点、操作人 | ✅ |
| 今日统计 | 统计今日报到人数 | ✅ |
| 跳过核验码 | 支持无核验码报到（测试模式） | ✅ |

#### 3.1.3 数据统计模块 ✅

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 实时数据 | 总人数/已报到/待报到/报到率 | ✅ |
| 学院统计 | 各学院报到人数和报到率 | ✅ |
| 生源地统计 | Top 10 省份报到情况 | ✅ |
| 近期记录 | 最近10条报到记录 | ✅ |
| 数据大屏 | 可视化展示界面 | ✅ |

#### 3.1.4 Django管理后台 ✅

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 学生管理 | CRUD操作 | ✅ |
| 专业管理 | CRUD操作 | ✅ |
| 学院管理 | CRUD操作 | ✅ |
| 报到记录管理 | 查看/删除记录 | ✅ |
| 所有模型管理 | 全模型CRUD | ✅ |

### 3.2 待完善功能模块

#### 3.2.1 宿舍管理模块 ⚠️

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 宿舍楼栋管理 | 楼栋信息维护 | ⚠️ 需填充数据 |
| 房间信息管理 | 房间状态维护 | ⚠️ 需填充数据 |
| 床位分配 | 手动/自动分配 | ⚠️ 需填充数据 |
| 宿舍查询 | 学生查看分配结果 | ⚠️ 需填充数据 |

#### 3.2.2 缴费管理模块 ⚠️

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 学费缴纳 | 学费项目设置 | ⚠️ 需填充数据 |
| 住宿费缴纳 | 住宿费设置 | ⚠️ 需填充数据 |
| 教材费缴纳 | 教材费设置 | ⚠️ 需填充数据 |
| 订单管理 | 缴费订单跟踪 | ⚠️ 需填充数据 |

#### 3.2.3 公告通知模块 ⚠️

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 公告发布 | 创建/编辑/发布公告 | ⚠️ 需填充数据 |
| 定向推送 | 按学院/专业推送 | ⚠️ 需填充数据 |
| 优先级设置 | 高/普通/低优先级 | ⚠️ 需填充数据 |
| 定时发布 | 设置发布时间 | ⚠️ 需填充数据 |

#### 3.2.4 知识库/FAQ模块 ⚠️

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 问题管理 | FAQ维护 | ⚠️ 需填充数据 |
| 分类管理 | 分类设置 | ⚠️ 需填充数据 |
| 关键词搜索 | 智能检索 | ⚠️ 需填充数据 |
| 统计功能 | 查看次数统计 | ⚠️ 需填充数据 |

#### 3.2.5 微信小程序模块 ⚠️

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 微信登录 | 小程序授权登录 | ⚠️ 需配置AppID |
| 学生绑定 | 学号密码绑定 | ⚠️ 需配置AppID |
| 报到码生成 | 生成动态报到码 | ⚠️ 需配置AppID |
| 扫码报到 | 扫码核验报到 | ⚠️ 需配置AppID |
| 缴费查询 | 查看缴费记录 | ⚠️ 需配置AppID |
| 宿舍查询 | 查看宿舍分配 | ⚠️ 需配置AppID |

---

## 四、数据库设计

### 4.1 数据模型总览

| 模型 | 表名 | 字段数 | 数据状态 | 说明 |
|:---|:---|:---:|:---:|:---|
| College | college | 5 | ✅ | 学院信息 |
| Major | major | 6 | ✅ | 专业信息 |
| Student | student | 16 | ✅ | 学生信息 |
| CheckIn | check_in | 6 | ✅ | 报到记录 |
| DormitoryBuilding | dormitory_building | 7 | ❌ | 宿舍楼栋 |
| DormitoryRoom | dormitory_room | 11 | ❌ | 宿舍房间 |
| DormitoryAssignment | dormitory_assignment | 6 | ❌ | 宿舍分配 |
| Payment | payment | 10 | ❌ | 缴费记录 |
| KnowledgeBase | knowledge_base | 9 | ❌ | 知识库 |
| FAQ | faq | 7 | ❌ | 常见问题 |
| Announcement | announcement | 11 | ❌ | 公告 |
| SystemConfig | system_config | 6 | ❌ | 系统配置 |

### 4.2 核心表结构

#### 4.2.1 学院表 (college)

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| id | Integer | 主键 |
| name | Char(100) | 学院名称 |
| code | Char(20) | 学院代码（唯一） |
| description | Text | 学院简介 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 4.2.2 专业表 (major)

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| id | Integer | 主键 |
| name | Char(100) | 专业名称 |
| code | Char(20) | 专业代码（唯一） |
| college_id | ForeignKey | 所属学院 |
| description | Text | 专业简介 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 4.2.3 学生表 (student)

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| id | Integer | 主键 |
| user_id | ForeignKey | Django用户（OneToOne） |
| student_id | Char(20) | 学号（唯一） |
| name | Char(50) | 姓名 |
| gender | Char(10) | 性别 |
| id_card | Char(18) | 身份证号 |
| phone | Char(20) | 联系电话 |
| major_id | ForeignKey | 专业 |
| class_name | Char(50) | 班级 |
| origin_province | Char(50) | 生源省份 |
| origin_city | Char(50) | 生源城市 |
| high_school | Char(100) | 毕业高中 |
| status | Char(20) | 报到状态 |
| check_in_time | DateTime | 报到时间 |
| dynamic_code | Char(32) | 动态核验码 |
| dynamic_code_expires | DateTime | 核验码过期时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 4.2.4 报到记录表 (check_in)

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| id | Integer | 主键 |
| student_id | ForeignKey | 学生 |
| check_in_method | Char(20) | 报到方式 |
| location | Char(100) | 报到地点 |
| operator | Char(50) | 操作人 |
| remarks | Text | 备注 |
| created_at | DateTime | 报到时间 |

### 4.3 数据表关系图

```
                    ┌──────────────┐
                    │   College   │
                    │   (学院)    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    Major     │
                    │   (专业)     │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │  Student  │  │   FAQ    │  │  Payment  │
    │  (学生)   │  │ (常见问题) │  │  (缴费)   │
    └─────┬─────┘  └───────────┘  └─────┬─────┘
          │
    ┌─────▼─────┐
    │ CheckIn   │
    │ (报到记录) │
    └───────────┘
```

---

## 五、API接口设计

### 5.1 REST API 接口

| 接口路径 | 方法 | 功能 | 状态 |
|:---|:---:|:---|:---:|
| `/api/colleges/` | GET/POST | 学院列表/创建 | ✅ |
| `/api/colleges/{id}/` | GET/PUT/DELETE | 学院详情/更新/删除 | ✅ |
| `/api/majors/` | GET/POST | 专业列表/创建 | ✅ |
| `/api/majors/{id}/` | GET/PUT/DELETE | 专业详情/更新/删除 | ✅ |
| `/api/students/` | GET/POST | 学生列表/创建 | ✅ |
| `/api/students/{id}/` | GET/PUT/DELETE | 学生详情/更新/删除 | ✅ |
| `/api/students/{id}/generate_dynamic_code/` | POST | 生成核验码 | ✅ |
| `/api/dormitory-buildings/` | GET/POST | 宿舍楼栋列表/创建 | ⚠️ |
| `/api/dormitory-rooms/` | GET/POST | 宿舍房间列表/创建 | ⚠️ |
| `/api/dormitory-assignments/` | GET/POST | 宿舍分配列表/创建 | ⚠️ |
| `/api/payments/` | GET/POST | 缴费记录列表/创建 | ⚠️ |
| `/api/check-ins/` | GET/POST | 报到记录列表/创建 | ✅ |
| `/api/check-ins/verify_and_checkin/` | POST | 验证并报到 | ✅ |
| `/api/knowledge-base/` | GET/POST | 知识库列表/创建 | ⚠️ |
| `/api/faqs/` | GET/POST | FAQ列表/创建 | ⚠️ |
| `/api/announcements/` | GET/POST | 公告列表/创建 | ⚠️ |
| `/api/system-configs/` | GET/POST | 系统配置列表/创建 | ⚠️ |
| `/api/dashboard/stats/` | GET | 数据统计 | ✅ |

### 5.2 微信小程序 API

| 接口路径 | 方法 | 功能 | 状态 |
|:---|:---:|:---|:---:|
| `/api/wechat/login/` | POST | 微信登录 | ⚠️ |
| `/api/wechat/bind/` | POST | 绑定学生信息 | ⚠️ |
| `/api/wechat/dashboard/` | GET | 个人 dashboard | ⚠️ |
| `/api/wechat/generate_code/` | POST | 生成动态报到码 | ⚠️ |
| `/api/wechat/verify_checkin/` | POST | 扫码验证报到 | ⚠️ |
| `/api/wechat/payments/` | GET | 缴费列表 | ⚠️ |
| `/api/wechat/dormitory/` | GET | 宿舍信息 | ⚠️ |
| `/api/wechat/logout/` | POST | 登出 | ⚠️ |

> ⚠️ 微信小程序接口需要配置 AppID 和 Secret 才能使用

### 5.3 前端页面路由

| 路由 | 视图 | 页面 | 状态 |
|:---|:---|:---|:---:|
| `/` | AdminIndexView | 数据大屏 | ✅ |
| `/checkin/` | AdminCheckinView | 扫码报到 | ✅ |
| `/students/` | AdminStudentsView | 学生管理 | ✅ |
| `/admin/` | admin.site.urls | Django管理后台 | ✅ |

---

## 六、核心业务流程

### 6.1 报到流程（已闭环）

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  录入学生信息  │ → │  人工/扫码报到 │ → │  状态变已报到  │
│  (Django后台)  │    │  (报到页面)   │    │  (系统自动)   │
└──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │  记录报到时间  │
                                       │  (CheckIn表)  │
                                       └──────────────┘
```

**详细步骤：**

1. **学生信息录入** - 管理员在Django后台录入学生基本信息
2. **生成动态码（可选）** - 学生可在微信小程序生成30分钟有效期的报到码
3. **人工/扫码报到** - 管理员使用报到页面，输入学号（或扫描报到码）
4. **状态更新** - 系统自动将学生状态变更为"已报到"
5. **记录报到** - 在CheckIn表中记录报到时间、地点、操作人

### 6.2 数据统计流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  查询Student  │ → │  聚合统计    │ → │  数据大屏展示  │
│  数据库       │    │  各学院/省份  │    │  实时更新     │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 七、部署配置

### 7.1 开发环境

```bash
# 启动服务
python manage.py runserver 8001

# 访问地址
# 数据大屏: http://127.0.0.1:8001/
# Django后台: http://127.0.0.1:8001/admin/
```

### 7.2 生产环境（推荐）

```bash
# 使用 Nginx + Gunicorn 部署
# 安装 gunicorn
pip install gunicorn

# 启动 gunicorn
gunicorn welcome_assistant.wsgi:application --bind 127.0.0.1:8001

# Nginx 配置参考 deploy/nginx.conf
```

### 7.3 Docker 部署

```bash
# 构建镜像
docker build -t welcome-assistant .

# 运行容器
docker run -d -p 8001:8001 welcome-assistant
```

---

## 八、访问地址

| 功能 | 地址 | 状态 |
|:---|:---|:---:|
| 数据大屏 | http://127.0.0.1:8001/ | ✅ |
| 扫码报到 | http://127.0.0.1:8001/checkin/ | ✅ |
| 学生管理 | http://127.0.0.1:8001/students/ | ✅ |
| Django管理后台 | http://127.0.0.1:8001/admin/ | ✅ |
| 管理员账号 | admin / admin123 | ✅ |

---

## 九、开发进度

### 9.1 MVP阶段（已完成）

| 阶段 | 周期 | 任务 | 状态 |
|:---|:---:|:---|:---:|
| Week 1 | 环境搭建 | Django项目初始化、PostgreSQL配置 | ✅ |
| Week 2 | 核心API | 学生管理、报到管理API | ✅ |
| Week 3 | 管理端 | 学生管理页面、报到页面、统计大屏 | ✅ |
| Week 4 | 测试优化 | Bug修复、Django管理后台配置 | ✅ |

### 9.2 下一版本计划

| 阶段 | 周期 | 任务 |
|:---|:---:|:---|
| Week 5 | 数据填充 | 宿舍楼栋、房间、缴费、公告、FAQ数据 |
| Week 6 | 微信小程序 | 配置AppID、登录、绑定、报到功能 |
| Week 7 | 部署上线 | Nginx部署、生产环境配置 |

---

## 十、技术债务与待办事项

### 10.1 已解决问题

| 序号 | 问题 | 状态 |
|:---:|:---|:---:|
| 1 | PostgreSQL数据库连接配置 | ✅ |
| 2 | Django管理后台显示数据大屏问题 | ✅ |
| 3 | 数据大屏各学院报到率为0% | ✅ |
| 4 | CSRF Token缺失导致403错误 | ✅ |
| 5 | 动态报到码功能 | ✅ 已实现（可选） |

### 10.2 待解决问题

| 序号 | 问题 | 状态 |
|:---:|:---|:---:|
| 1 | 微信小程序AppID配置 | ⚠️ |
| 2 | 宿舍管理数据填充 | ⚠️ |
| 3 | 缴费管理数据填充 | ⚠️ |
| 4 | 公告通知数据填充 | ⚠️ |
| 5 | 知识库/FAQ数据填充 | ⚠️ |

---

## 十一、验收标准

| 序号 | 验收条件 | 状态 |
|:---:|:---|:---:|
| 1 | 管理员可录入、查看、搜索学生信息 | ✅ |
| 2 | 管理员可完成人工报到登记 | ✅ |
| 3 | 数据大屏实时显示报到统计 | ✅ |
| 4 | Django管理后台可管理所有数据 | ✅ |
| 5 | 学生可查询宿舍分配结果 | ⚠️ |
| 6 | 学生可查询缴费记录 | ⚠️ |
| 7 | 微信小程序报到功能 | ⚠️ |

---

## 十二、附录

### 12.1 配置参考

#### PostgreSQL pg_hba.conf 配置

```conf
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
```

#### 微信小程序配置

```python
# welcome_app/wechat_views.py
WECHAT_APPID = 'your_appid'      # 需要替换为真实AppID
WECHAT_SECRET = 'your_secret'    # 需要替换为真实Secret
```

### 12.2 常用命令

```bash
# 迁移数据库
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser
# 或
python create_superuser.py

# 启动服务器
python manage.py runserver 8001

# 收集静态文件
python manage.py collectstatic
```

---

**文档版本**: V2.0
**编制日期**: 2026-04-23
**适用范围**: 大学生新生报到智能助手 - 完整技术方案
