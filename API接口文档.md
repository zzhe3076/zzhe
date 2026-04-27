# API接口文档

## 一、接口概览

| 前缀 | 说明 |
|:---|:---|
| `/api/` | REST API 接口 |
| `/api/wechat/` | 微信小程序API |
| `/student/` | 学生端页面 |

---

## 二、REST API

基础URL: `http://127.0.0.1:8001/api/`

### 1. 学院管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/colleges/` | GET | 获取学院列表 |
| `/api/colleges/` | POST | 创建学院 |
| `/api/colleges/{id}/` | GET | 获取学院详情 |
| `/api/colleges/{id}/` | PUT | 更新学院 |
| `/api/colleges/{id}/` | DELETE | 删除学院 |

**请求示例**:
```json
POST /api/colleges/
{
    "name": "计算机学院",
    "code": "CS"
}
```

---

### 2. 专业管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/majors/` | GET | 获取专业列表 |
| `/api/majors/` | POST | 创建专业 |
| `/api/majors/{id}/` | GET | 获取专业详情 |
| `/api/majors/{id}/` | PUT | 更新专业 |
| `/api/majors/{id}/` | DELETE | 删除专业 |

**请求示例**:
```json
POST /api/majors/
{
    "name": "软件工程",
    "code": "SE2024",
    "college": 1
}
```

---

### 3. 学生管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/students/` | GET | 获取学生列表 |
| `/api/students/` | POST | 创建学生 |
| `/api/students/{id}/` | GET | 获取学生详情 |
| `/api/students/{id}/` | PUT | 更新学生 |
| `/api/students/{id}/` | DELETE | 删除学生 |

**查询参数**:
| 参数 | 说明 |
|:---|:---|
| `search` | 搜索（姓名/学号） |
| `status` | 报到状态 |
| `major` | 专业ID |
| `page` | 页码 |

**请求示例**:
```json
POST /api/students/
{
    "student_id": "2024001",
    "name": "张三",
    "gender": "male",
    "id_card": "110101200001011234",
    "phone": "13800138001",
    "major": 1,
    "origin_province": "北京"
}
```

---

### 4. 报到管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/check-ins/` | GET | 获取报到记录 |
| `/api/check-ins/` | POST | 创建报到记录 |
| `/api/check-ins/verify_and_checkin/` | POST | 验证并报到 |

**验证报到请求**:
```json
POST /api/check-ins/verify_and_checkin/
{
    "student_id": "2024001",
    "check_in_method": "manual",
    "location": "报到处A",
    "operator": "管理员"
}
```

---

### 5. 数据统计

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/dashboard/stats/` | GET | 获取统计概览 |

**响应示例**:
```json
GET /api/dashboard/stats/

{
    "total_students": 100,
    "checked_in": 45,
    "pending": 55,
    "check_in_rate": 45.0,
    "today_checked_in": 10
}
```

---

### 6. 宿舍管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/dormitory-buildings/` | GET/POST | 宿舍楼栋 |
| `/api/dormitory-buildings/{id}/` | GET/PUT/DELETE | 楼栋详情 |
| `/api/dormitory-rooms/` | GET/POST | 宿舍房间 |
| `/api/dormitory-rooms/{id}/` | GET/PUT/DELETE | 房间详情 |
| `/api/dormitory-assignments/` | GET/POST | 宿舍分配 |
| `/api/dormitory-assignments/{id}/` | GET/PUT/DELETE | 分配详情 |

---

### 7. 缴费管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/payments/` | GET | 获取缴费列表 |
| `/api/payments/` | POST | 创建缴费记录 |
| `/api/payments/{id}/` | GET/PUT/DELETE | 缴费详情 |

---

### 8. 公告管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/announcements/` | GET | 获取公告列表 |
| `/api/announcements/` | POST | 创建公告 |
| `/api/announcements/{id}/` | GET/PUT/DELETE | 公告详情 |

---

### 9. FAQ管理

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/faqs/` | GET | 获取FAQ列表 |
| `/api/faqs/` | POST | 创建FAQ |
| `/api/faqs/{id}/` | GET/PUT/DELETE | FAQ详情 |

---

### 10. 知识库

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/knowledge-base/` | GET | 获取知识库 |
| `/api/knowledge-base/` | POST | 添加知识 |
| `/api/knowledge-base/{id}/` | GET/PUT/DELETE | 知识详情 |

---

### 11. 系统配置

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/system-configs/` | GET | 获取配置列表 |
| `/api/system-configs/` | POST | 创建配置 |
| `/api/system-configs/{id}/` | GET/PUT/DELETE | 配置详情 |

---

## 三、微信小程序API

基础URL: `http://127.0.0.1:8001/api/wechat/`

| 接口 | 方法 | 说明 |
|:---|:---:|:---|
| `/api/wechat/login/` | POST | 微信登录 |
| `/api/wechat/bind/` | POST | 绑定学生 |
| `/api/wechat/logout/` | POST | 退出登录 |
| `/api/wechat/dashboard/` | GET | 个人中心 |
| `/api/wechat/generate_code/` | POST | 生成报到码 |
| `/api/wechat/verify_checkin/` | POST | 扫码报到 |
| `/api/wechat/payments/` | GET | 缴费列表 |
| `/api/wechat/dormitory/` | GET | 宿舍信息 |

---

## 四、学生端页面

基础URL: `http://127.0.0.1:8001/`

| 路由 | 页面 | 说明 |
|:---|:---|:---|
| `/student/login/` | 登录页 | 学号+手机号登录 |
| `/student/` | 首页 | 报到状态 |
| `/student/dormitory/` | 宿舍 | 宿舍查询 |
| `/student/payment/` | 缴费 | 缴费查询 |
| `/student/announcement/` | 公告 | 公告列表 |
| `/student/faq/` | 问答 | FAQ列表 |
| `/student/logout/` | 退出 | 退出登录 |

---

## 五、响应格式

### 成功响应

```json
{
    "success": true,
    "data": { ... }
}
```

### 列表响应

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8001/api/students/?page=2",
    "previous": null,
    "results": [ ... ]
}
```

### 错误响应

```json
{
    "success": false,
    "error": "错误信息"
}
```

---

## 六、状态码

| 状态码 | 说明 |
|:---:|:---|
| 200 | OK - 请求成功 |
| 201 | Created - 创建成功 |
| 400 | Bad Request - 请求错误 |
| 401 | Unauthorized - 未授权 |
| 404 | Not Found - 资源不存在 |
| 500 | Server Error - 服务器错误 |

---

**版本**: V1.0 | **日期**: 2026-04-27
