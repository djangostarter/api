import contextvars
from typing import Optional


request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("request_id", default=None)


def set_request_id(value: Optional[str]) -> None:
    request_id_var.set(value)


def get_request_id() -> Optional[str]:
    return request_id_var.get()


class RequestIdFilter:
    def filter(self, record) -> bool:
        record.request_id = get_request_id() or "-"
        return True

