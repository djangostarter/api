# DjangoStarter API（django-starter-api）

`django-starter-api` 是一个专注于 **纯 API（Headless）开发** 的 Django + Django-Ninja 起手架：保留 Django 的成熟生态与工程化能力，同时提供 FastAPI 风格的类型安全 API、OpenAPI 文档与清晰的模块边界。

它的定位是 DjangoStarter “三段式分发”中的 **API-only 模板**：

- Core：`django-starter-core`（可复用底座能力）
- API-only：`django-starter-api`（本项目，仅接口，不含前端）
- Web：`django-starter-web`（全栈模板，模板渲染 + 前端构建链路）

> 包名与 import 命名空间说明：
>
> - 安装包名（PyPI / 依赖声明）：`django-starter-api`、`django-starter-core`
> - Core 的 Python import 命名空间：`django_starter_core`

## 特性

- **API-only**：不包含模板渲染与前端依赖，适合前后端分离或纯后端服务
- **Django-Ninja**：类型校验 + 自动 OpenAPI 文档（Swagger UI）
- **版本化路由**：约定所有接口挂载在 `/api/v1/` 下（便于后续扩展 v2）
- **内置示例模块**
  - `health`：健康检查接口
  - `authentication`：JWT 鉴权骨架（用户名密码换 Token、受保护示例接口）
  - `demo_crud`：最小 CRUD 示例
- **复用 Core**：统一响应封装、JWT 生成/解析、Bearer 鉴权等能力来自 `django-starter-core`
- **开箱即用的 CORS**：默认允许所有来源（开发友好，生产建议收紧）

## 运行环境

见 `pyproject.toml`：

- Python：`==3.14.*`
- Django：`django[argon2]>=6.0`
- Django-Ninja：`>=1.5.3`

## 快速开始（本仓库）

1）安装依赖：

```bash
uv sync
```

2）迁移数据库（默认 SQLite）：

```bash
uv run python .\src\manage.py migrate
```

3）启动开发服务器：

```bash
uv run python .\src\manage.py runserver
```

4）打开 OpenAPI 文档：

- http://127.0.0.1:8000/api/v1/docs

## 目录结构与约定

本项目采用 “按领域拆分 apps + 统一 API 入口” 的组织方式：

- `src/config/`：Django 工程配置（settings/urls/asgi/wsgi）
- `src/api/v1.py`：API v1 入口（NinjaAPI 实例、异常处理、路由汇总）
- `src/apps/*`：业务模块（每个 app 自己管理 models/schemas/apis 等）

路由挂载约定（见 `src/config/urls.py`）：

- Django 管理后台：`/admin/`
- 对外 API：`/api/v1/`

## 开发一个新接口（推荐方式）

1）新建一个 Django app（例如 `apps/orders`）
2）在 app 内新增一个 `apis.py`，暴露 `router = Router(...)`
3）在 `src/api/v1.py` 中 `api_v1.add_router("/orders", orders_router)`

这样可以保证：

- API 入口集中可读（`api/v1.py`）
- 业务模块自治（各自 schemas/models/apis）

## 配置项与环境变量

本项目大量配置支持用环境变量覆盖（见 `src/config/settings.py`），常用项如下：

- `DJANGO_SECRET_KEY`：Django 密钥（生产务必设置）
- `DJANGO_DEBUG`：`1`/`0`
- `DJANGO_ALLOWED_HOSTS`：逗号分隔，默认 `*`
- `DJANGO_DB_ENGINE`：默认 `django.db.backends.sqlite3`
- `DJANGO_DB_NAME`：默认 `src/db.sqlite3`
- `DJANGO_CORS_ALLOW_ALL_ORIGINS`：默认 `1`（生产建议改为白名单）

## JWT 配置（与 Core 约定保持一致）

Core 的 JWT 逻辑读取 `settings.DJANGO_STARTER['auth']['jwt']`，本项目已在 settings 中提供同结构配置，并暴露以下环境变量：

- `DJANGO_JWT_ALGO`：算法，默认 `HS256`
- `DJANGO_JWT_SALT`：签名密钥（生产务必设置为强随机值，且不要提交到仓库）
- `DJANGO_JWT_LIFETIME`：有效期（秒），默认 `3600`

示例接口（见 `apps/authentication/apis.py`）：

- `POST /api/v1/auth/token`：用户名密码换 JWT
- `GET  /api/v1/auth/me`：受保护示例接口（Bearer Token）

## 与 django-starter-core 的联调方式（你开发 Core 时最重要）

本项目默认启用了 uv 的 “本地路径 editable 覆盖”，这样你在同一工作区修改 Core 代码时，无需发布即可在 API 项目中实时生效：

```toml
[tool.uv.sources]
django-starter-core = { path = "../django-starter-core", editable = true }
```

发布/交付给用户时，一般只保留正常的版本依赖（例如 `django-starter-core>=0.1.0`），让用户通过升级版本号跟随 Core 迭代。

## 运行测试

```bash
uv run pytest
```
