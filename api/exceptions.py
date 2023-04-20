from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ForbiddenException(APIException):
    status_code = 403
    default_detail = "Access Denied"
    default_code = "access_denied"


class UnauthorizedException(APIException):
    status_code = 401
    default_detail = "Unauthorized"
    default_code = "access_unauthorized"


def custom_exception_handler(exc, context):
    if isinstance(exc, (ForbiddenException, UnauthorizedException)):
        response = Response(
            {"detail": exc.detail, "code": exc.default_code},
            status=exc.status_code
        )
        return response
    return exception_handler(exc, context)
