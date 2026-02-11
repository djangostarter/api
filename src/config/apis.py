"""
兼容导出：保留该模块以便后续扩展/迁移时不影响旧的 import 路径。

当前推荐直接使用：
- from api.v1 import api_v1
"""

from api.v1 import api_v1


# 为了兼容早期的 `from config.apis import api` 写法
api = api_v1
