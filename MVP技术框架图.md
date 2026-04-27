# 大学生新生报到智能助手 - MVP技术框架图

## 一、系统整体架构图

```mermaid
graph TB
    subgraph Client["用户接入层"]
        direction TB
        H5["学生Web端(H5)<br/>📱 新生端"]
        WEB["Web管理端<br/>💻 管理员"]
    end

    subgraph Gateway["网关层"]
        direction TB
        NGINX["Nginx<br/>负载均衡/静态资源"]
    end

    subgraph App["应用层"]
        direction TB
        DJANGO["Django + DRF<br/>REST API"]
        
        subgraph API["API模块"]
            direction TB
            STU_API["学生管理API"]
            CHK_API["报到核验API"]
            STAT_API["数据统计API"]
            DORM_API["宿舍管理API"]
            PAY_API["缴费管理API"]
            ANN_API["公告通知API"]
            FAQ_API["FAQ知识库API"]
            WX_API["微信小程序API"]
        end
        
        subgraph Auth["认证模块"]
            SESSION["Session认证"]
            TOKEN["Token认证"]
        end
    end

    subgraph Business["业务逻辑层"]
        direction TB
        STU_MGR["学生管理"]
        CHK_MGR["报到管理"]
        STAT_MGR["数据统计"]
        DORM_MGR["宿舍分配"]
        PAY_MGR["缴费管理"]
        ANN_MGR["公告管理"]
        FAQ_MGR["问答管理"]
    end

    subgraph Data["数据层"]
        direction TB
        PG["PostgreSQL 18<br/>数据库"]
        
        subgraph Tables["数据表"]
            direction TB
            T1["Student<br/>学生表"]
            T2["College<br/>学院表"]
            T3["Major<br/>专业表"]
            T4["CheckIn<br/>报到记录表"]
            T5["Dormitory<br/>宿舍表"]
            T6["Payment<br/>缴费表"]
            T7["Announcement<br/>公告表"]
            T8["FAQ<br/>问答表"]
            T9["KnowledgeBase<br/>知识库表"]
            T10["SystemConfig<br/>系统配置表"]
        end
    end

    subgraph Templates["前端展示层"]
        direction TB
        HTML["HTML模板<br/>Bootstrap 5"]
        
        subgraph Pages["页面"]
            direction TB
            P1["数据大屏<br/>index.html"]
            P2["报到页面<br/>checkin.html"]
            P3["学生管理<br/>students.html"]
            P4["Admin后台<br/>Django Admin"]
        end
    end

    WX --> NGINX
    WEB --> NGINX
    NGINX --> DJANGO
    
    DJANGO --> API
    API --> Auth
    API --> Business
    Business --> STAT_MGR
    Business --> STU_MGR
    Business --> CHK_MGR
    Business --> DORM_MGR
    Business --> PAY_MGR
    Business --> ANN_MGR
    Business --> FAQ_MGR
    
    Business --> PG
    PG --> Tables
    
    DJANGO --> HTML
    HTML --> Pages
```

---

## 二、技术栈架构图

```mermaid
graph LR
    subgraph Frontend["前端技术栈"]
        direction TB
        F1["Bootstrap 5"]
        F2["JavaScript"]
        F3["HTML5/CSS3"]
        F4["微信小程序<br/>WXML/WXSS/JS"]
    end

    subgraph Backend["后端技术栈"]
        direction TB
        B1["Django 6.0.4"]
        B2["Django REST Framework"]
        B3["Python 3.x"]
        B4["psycopg2<br/>PostgreSQL驱动"]
    end

    subgraph Database["数据库"]
        D1["PostgreSQL 18"]
        D2["Redis<br/>缓存(可选)"]
    end

    subgraph DevOps["部署运维"]
        direction TB
        D3["Nginx"]
        D4["Docker"]
        D5["Linux Server"]
    end

    Frontend --> Backend
    Backend --> Database
    Backend --> DevOps
```

---

## 三、数据流架构图

```mermaid
sequenceDiagram
    participant 新生 as 新生(微信小程序)
    participant 管理员 as 管理员(Web后台)
    participant Nginx as Nginx网关
    participant Django as Django+DRF
    participant DB as PostgreSQL

    Note over 新生,Django: 报到流程
    
    新生->>Nginx: 1. 访问报到页面
    Nginx->>Django: 2. 转发请求
    Django->>DB: 3. 查询学生信息
    DB-->>Django: 4. 返回数据
    Django-->>Nginx: 5. 返回页面
    Nginx-->>新生: 6. 显示报到页面
    
    新生->>Nginx: 7. 提交报到(扫码/人脸)
    Nginx->>Django: 8. 转发请求
    Django->>DB: 9. 验证并更新报到状态
    DB-->>Django: 10. 返回结果
    Django-->>Nginx: 11. 返回结果
    Nginx-->>新生: 12. 报到成功提示

    Note over 管理员,Django: 管理流程
    
    管理员->>Nginx: 访问管理后台
    Nginx->>Django: 转发请求
    Django->>DB: 查询/管理数据
    DB-->>Django: 返回数据
    Django-->>Nginx: 返回页面
    Nginx-->>管理员: 显示管理后台
```

---

## 四、功能模块架构图

```mermaid
graph TB
    subgraph System["大学生新生报到系统"]
        
        subgraph Student["学生管理模块"]
            S1["信息录入"]
            S2["信息查询"]
            S3["信息修改"]
            S4["状态管理"]
        end
        
        subgraph CheckIn["报到核验模块"]
            C1["人工报到"]
            C2["扫码报到"]
            C3["动态码报到"]
            C4["报到记录"]
        end
        
        subgraph Stats["数据统计模块"]
            T1["实时大屏"]
            T2["学院统计"]
            T3["生源地统计"]
            T4["报到率计算"]
        end
        
        subgraph Dorm["宿舍管理模块"]
            D1["宿舍楼栋"]
            D2["房间分配"]
            D3["分配查询"]
        end
        
        subgraph Payment["缴费管理模块"]
            P1["缴费记录"]
            P2["缴费查询"]
            P3["状态同步"]
        end
        
        subgraph Notice["通知公告模块"]
            N1["发布公告"]
            N2["查看公告"]
            N3["推送通知"]
        end
        
        subgraph FAQ["问答模块"]
            F1["知识库"]
            F2["常见问题"]
            F3["智能问答"]
        end
        
    end
```

---

## 五、网络拓扑架构图

```mermaid
graph TB
    Internet["🌐 互联网"]
    
    subgraph DMZ["DMZ区"]
        LB["负载均衡器<br/>Nginx"]
    end
    
    subgraph AppZone["应用区"]
        Server["应用服务器<br/>Django"]
    end
    
    subgraph DataZone["数据区"]
        DB["数据库服务器<br/>PostgreSQL"]
    end
    
    subgraph MgmtZone["管理区"]
        AdminPC["管理员电脑"]
    end
    
    Mobile["📱 学生手机"]
    
    Internet --> Mobile
    Internet --> DMZ
    DMZ --> LB
    LB --> Server
    Server --> DB
    AdminPC --> DMZ
    AdminPC --> MgmtZone
    
    style Internet fill:#f9f,stroke:#333
    style DMZ fill:#ff9,stroke:#333
    style AppZone fill:#9ff,stroke:#333
    style DataZone fill:#9f9,stroke:#333
    style MgmtZone fill:#f99,stroke:#333
```

---

## 六、数据库ER图

```mermaid
erDiagram
    COLLEGE ||--o{ MAJOR : contains
    COLLEGE ||--o{ STUDENT : has
    MAJOR ||--o{ STUDENT : belongs
    STUDENT ||--o| CHECKIN : has
    STUDENT ||--o| DORMITORY_ASSIGNMENT : receives
    STUDENT ||--o| PAYMENT : makes
    STUDENT ||--o| FAQ : queries
    
    COLLEGE {
        int id PK
        string name
        string code
        datetime created_at
    }
    
    MAJOR {
        int id PK
        string name
        string code
        int college_id FK
        datetime created_at
    }
    
    STUDENT {
        int id PK
        string name
        string student_number
        string id_card
        string phone
        int college_id FK
        int major_id FK
        string status
        datetime created_at
    }
    
    CHECKIN {
        int id PK
        int student_id FK
        string checkin_method
        datetime checkin_time
        string operator
        string remarks
    }
    
    DORMITORY_BUILDING {
        int id PK
        string name
        string building_type
        int total_rooms
    }
    
    DORMITORY_ROOM {
        int id PK
        int building_id FK
        string room_number
        int capacity
        int current_count
    }
    
    DORMITORY_ASSIGNMENT {
        int id PK
        int student_id FK
        int room_id FK
        string bed_number
        datetime assigned_at
    }
    
    PAYMENT {
        int id PK
        int student_id FK
        string payment_type
        decimal amount
        string status
        datetime paid_at
    }
    
    ANNOUNCEMENT {
        int id PK
        string title
        text content
        string publish_status
        datetime publish_time
    }
    
    FAQ {
        int id PK
        string question
        text answer
        string category
        int sort_order
    }
```

---

## 七、API接口架构图

```mermaid
graph TB
    subgraph REST_API["REST API 接口"]
        
        subgraph StudentAPI["学生管理"]
            SA1["GET /api/students/"]
            SA2["POST /api/students/"]
            SA3["GET /api/students/{id}/"]
            SA4["PUT /api/students/{id}/"]
            SA5["DELETE /api/students/{id}/"]
        end
        
        subgraph CollegeAPI["学院管理"]
            CA1["GET /api/colleges/"]
            CA2["POST /api/colleges/"]
        end
        
        subgraph MajorAPI["专业管理"]
            MA1["GET /api/majors/"]
            MA2["POST /api/majors/"]
        end
        
        subgraph CheckInAPI["报到管理"]
            CIA1["GET /api/check-ins/"]
            CIA2["POST /api/check-ins/"]
            CIA3["POST /api/check-ins/verify_and_checkin/"]
        end
        
        subgraph StatsAPI["数据统计"]
            STA1["GET /api/dashboard/stats/"]
            STA2["GET /api/dashboard/college-stats/"]
            STA3["GET /api/dashboard/province-stats/"]
        end
        
    end
    
    subgraph WeChatAPI["微信小程序API"]
        
        subgraph WXAuth["认证模块"]
            WA1["POST /api/wechat/login/"]
            WA2["POST /api/wechat/bind/"]
            WA3["POST /api/wechat/logout/"]
        end
        
        subgraph WXCheckIn["报到模块"]
            WC1["GET /api/wechat/dashboard/"]
            WC2["POST /api/wechat/generate_code/"]
            WC3["POST /api/wechat/verify_checkin/"]
        end
        
        subgraph WXInfo["信息模块"]
            WI1["GET /api/wechat/dormitory/"]
            WI2["GET /api/wechat/payments/"]
            WI3["GET /api/wechat/announcements/"]
            WI4["GET /api/wechat/faqs/"]
        end
        
    end
```

---

## 八、系统部署架构图

```mermaid
graph TB
    subgraph Production["生产环境部署"]
        
        subgraph WebServer["Web服务器"]
            NGINX["Nginx<br/>:80/:443"]
        end
        
        subgraph AppServer["应用服务器"]
            GUNICORN["Gunicorn<br/>多进程"]
            UWSGI["uWSGI<br/>(可选)"]
        end
        
        subgraph Cache["缓存层"]
            REDIS["Redis<br/>(可选)"]
        end
        
        subgraph Database["数据库"]
            PG["PostgreSQL<br/>主库"]
            PG_REPL["PostgreSQL<br/>(从库-可选)"]
        end
        
        subgraph Static["静态资源"]
            STATIC["静态文件<br/>CSS/JS/Images"]
            MEDIA["媒体文件<br/>上传文件"]
        end
        
    end
    
    subgraph Monitor["监控运维"]
        LOG["日志系统"]
        METRIC["指标监控"]
    end
    
    NGINX --> GUNICORN
    NGINX --> STATIC
    NGINX --> MEDIA
    GUNICORN --> REDIS
    GUNICORN --> PG
    PG --> PG_REPL
    GUNICORN --> LOG
    LOG --> METRIC
```

---

*文档版本: V1.0*
*编制日期: 2026-04-25*
