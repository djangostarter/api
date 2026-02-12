# Django Ninja 配置
import os

from config.settings.components.common import DEBUG


_docs_raw = os.environ.get("DJANGO_NINJA_DOCS_ENABLED")
if _docs_raw is None:
    NINJA_DOCS_ENABLED = DEBUG
else:
    NINJA_DOCS_ENABLED = _docs_raw.strip().lower() in {"1", "true", "yes", "y", "on"}

NINJA_PAGINATION_PER_PAGE = 10
