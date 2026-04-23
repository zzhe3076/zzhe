# 大学生新生报到智能助手 - MVP技术方案

## 一、MVP目标定位

最小可行产品版本聚焦**核心报到流程闭环**，以最快速度验证业务价值。

**核心价值主张**：让新生一部手机完成报到，让校方实时掌握报到进度

---

## 二、MVP功能清单

### 2.1 学生端（微信小程序/Web）

| 序号 | 功能模块 | 优先级 | 说明 |
|:---:|:---|:---:|:---|
| 1 | 新生注册登录 | P0 | 手机号+身份证号验证身份 |
| 2 | 个人信息查看 | P0 | 查看基本资料、专业班级 |
| 3 | 在线报到 | P0 | 生成动态码 → 扫码核验 → 报到成功 |
| 4 | 宿舍分配查询 | P0 | 查看分配的楼栋、房间、床位 |
| 5 | 缴费查询 | P1 | 查看待缴费用、缴费状态 |
| 6 | 公告通知 | P1 | 接收学校通知公告 |
| 7 | 智能问答 | P1 | FAQ知识库检索 |

### 2.2 管理端（Web后台）

| 序号 | 功能模块 | 优先级 | 说明 |
|:---:|:---|:---:|:---|
| 1 | 学生管理 | P0 | 导入/查看/搜索学生信息 |
| 2 | 报到核验 | P0 | 扫码枪扫描学生动态码完成报到 |
| 3 | 宿舍分配 | P0 | 手动/自动分配宿舍 |
| 4 | 数据统计 | P0 | 实时报到进度大屏 |
| 5 | 公告管理 | P1 | 发布通知公告 |
| 6 | 知识库维护 | P1 | 管理FAQ问答 |

---

## 三、技术架构

### 3.1 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    用户接入层                            │
│   ┌─────────────┐          ┌──────────────────┐        │
│   │   微信小程序   │          │   Web管理端      │        │
│   └──────┬──────┘          └────────┬─────────┘        │
│          │                           │                  │
│          └───────────┬───────────────┘                  │
│                      ▼                                   │
│            ┌─────────────────┐                           │
│            │   Nginx网关     │  负载均衡/静态资源        │
│            └────────┬────────┘                           │
│                     ▼                                    │
│          ┌──────────────────┐                            │
│          │  Django API层   │  REST API + 业务逻辑        │
│          └────────┬─────────┘                            │
│                     ▼                                    │
│          ┌──────────────────┐                            │
│          │  SQLite/PG数据库 │  数据持久化                │
│          └──────────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

### 3.2 技术选型

| 层级 | 技术方案 | 说明 |
|:---|:---|:---|
| 前端（小程序） | 微信小程序原生开发 | 轻量化、即用即走 |
| 前端（管理端） | Bootstrap + jQuery | 快速开发、低维护成本 |
| 后端框架 | Django 4.x + DRF | 成熟稳定、快速开发 |
| 数据库 | SQLite（开发）→ PostgreSQL（生产） | 开发免配置，生产高性能 |
| Web服务器 | Nginx | 反向代理、静态资源服务 |
| 部署 | Docker | 容器化、一键部署 |

### 3.3 目录结构

```
welcome_assistant/
├── welcome_app/           # 主应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 业务视图
│   ├── serializers.py     # API序列化
│   ├── urls.py            # 路由配置
│   └── templates/          # HTML模板
├── welcome_assistant/     # 项目配置
│   ├── settings.py
│   └── wsgi.py
├── deploy/                # 部署配置
│   └── nginx.conf
├── Dockerfile             # 容器化配置
└── requirements.txt       # 依赖清单
```

---

## 四、数据库设计（精简版）

### 4.1 核心数据模型

| 模型 | 字段 | 说明 |
|:---|:---|:---|
| **Student** | student_id, name, phone, id_card, gender, major, status, check_in_time, dynamic_code | 学生信息/报到状态 |
| **Major** | name, code, college | 专业 |
| **College** | name, code | 学院 |
| **DormitoryRoom** | building, room_number, floor, capacity, current_occupancy, price | 宿舍房间 |
| **DormitoryAssignment** | student, room, bed_number, status | 宿舍分配 |
| **Payment** | student, payment_type, amount, status, order_number | 缴费记录 |
| **CheckIn** | student, check_in_method, location, operator, created_at | 报到记录 |
| **Announcement** | title, content, is_published, published_at | 公告 |
| **KnowledgeBase** | question, answer, category, keywords, is_active | 知识库 |

---

## 五、API接口设计

### 5.1 学生端接口

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/students/register/` | POST | 新生注册 |
| `/api/students/login/` | POST | 登录认证 |
| `/api/students/me/` | GET | 获取个人信息 |
| `/api/students/me/checkin/` | POST | 发起报到（获取动态码） |
| `/api/students/me/dormitory/` | GET | 查询宿舍分配 |
| `/api/students/me/payments/` | GET | 查询缴费记录 |
| `/api/announcements/` | GET | 获取公告列表 |
| `/api/knowledge/search/` | GET | 知识库检索 |

### 5.2 管理端接口

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/students/` | GET/POST | 学生列表/新增 |
| `/api/checkin/verify/` | POST | 扫码核验报到 |
| `/api/dormitory/assign/` | POST | 宿舍分配 |
| `/api/dashboard/stats/` | GET | 数据统计 |
| `/api/announcements/` | CRUD | 公告管理 |
| `/api/knowledge/` | CRUD | 知识库管理 |

---

## 六、核心业务流程

### 6.1 报到流程（核心闭环）

```
新生登录 → 生成30分钟有效期动态码 → 现场扫码核验 → 状态变更为"已报到" → 记录报到时间
```

### 6.2 宿舍分配流程（简化版）

```
管理员导入学生数据 → 手动/自动分配宿舍 → 学生查询结果
```

---

## 七、MVP开发计划

### 7.1 阶段划分

| 阶段 | 周期 | 任务 |
|:---|:---:|:---|
| **Week 1** | 环境搭建 | 项目初始化、Docker配置、Nginx配置 |
| **Week 2** | 核心API | 学生注册/登录、报到核验、宿舍分配API |
| **Week 3** | 管理端 | 学生管理、报到核验、宿舍分配、数据统计页面 |
| **Week 4** | 学生端 | 微信小程序注册/登录、报到、查询功能 |
| **Week 5** | 知识库+公告 | FAQ管理、公告发布 |
| **Week 6** | 测试部署 | 内部测试、Docker镜像构建、生产部署 |

### 7.2 预计工时

| 模块 | 人力 |
|:---|:---:|
| 后端API开发 | 3人日 |
| 管理端前端 | 3人日 |
| 微信小程序 | 4人日 |
| 部署运维 | 1人日 |
| **合计** | **约11人日** |

---

## 八、MVP技术债务说明

为快速上线，MVP阶段允许以下简化：

1. **认证方式**：使用简单Session认证，不引入JWT
2. **数据库**：开发环境使用SQLite，生产使用PostgreSQL
3. **缓存**：暂不引入Redis
4. **消息队列**：暂不使用异步任务
5. **监控**：暂不部署Prometheus/Grafana
6. **AI问答**：MVP阶段使用关键词检索，不接入大模型API

---

## 九、部署方案

### 9.1 Docker Compose一键部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./db.sqlite3:/app/db.sqlite3
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=your-domain.com

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./deploy/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
```

### 9.2 最低配置要求

| 资源 | 最低配置 |
|:---|:---|
| CPU | 2核 |
| 内存 | 4GB |
| 硬盘 | 40GB |
| 带宽 | 5Mbps |

---

## 十、验收标准

| 序号 | 验收条件 |
|:---:|:---|
| 1 | 新生可完成注册、登录、信息填报 |
| 2 | 管理员可完成扫码报到核验 |
| 3 | 学生可查询宿舍分配结果 |
| 4 | 管理后台可查看实时报到统计数据 |
| 5 | 系统可通过Docker一键部署 |

---

**文档版本**：V1.0  
**编制日期**：2026-04-22  
**适用范围**：MVP版本开发实施
