from ninja.errors import HttpError


class AppClientPermissionError(HttpError):
    def __init__(self, message: str = "权限不足"):
        super().__init__(403, message)

