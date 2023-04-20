from django.http import JsonResponse
from django.core.exceptions import ValidationError


class ValidationErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            return JsonResponse({"error": str(exception.message)}, status=400)
