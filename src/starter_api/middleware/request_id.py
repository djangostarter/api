import uuid

from django.http import HttpRequest

from starter_api.logging_context import set_request_id


class RequestIdMiddleware:
    header_name = "HTTP_X_REQUEST_ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request_id = request.META.get(self.header_name) or uuid.uuid4().hex
        request.META[self.header_name] = request_id
        set_request_id(request_id)

        try:
            response = self.get_response(request)
            response["X-Request-Id"] = request_id
            return response
        finally:
            set_request_id(None)

