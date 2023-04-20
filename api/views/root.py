from django.urls import reverse_lazy
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.schemas.boot_schema import api_root_response_schema


class ApiRootView(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of all API routes",
        responses={
            200: api_root_response_schema,
        },
        tags=["api endpoints"],
        security=[],
    )
    def get(self, request):
        """
        This view returns a list of all the routes in API.
        """
        protocol = request.scheme
        host = request.get_host()
        url = f'{protocol}://{host}'
        return Response({
            'register': {
                'url': f'{url}{reverse_lazy("api:api-register-user")}',
                'info': 'create new user and send activation token to email'
            },
            'activate': {
                'url': f'{url}{reverse_lazy("api:api-activate-user")}',
                'info': 'activate user by email and activation token'
            },
            'reactivate-token': {
                'url': f'{url}{reverse_lazy("api:api-reactivate-token")}',
                'info': 'send new activation token to user email'
            },
            'password-token': {
                'url': f'{url}{reverse_lazy("api:api-request-password-token")}',
                'info': 'send password reset token to user email'
            },
            'password-reset': {
                'url': f'{url}{reverse_lazy("api:api-password-reset")}',
                'info': 'reset current password by password reset token'
            },
            'jwt-obtain-pair': {
                'url': f'{url}{reverse_lazy("api:token_obtain_pair")}',
                'info': 'generate jwt pair tokens(refresh, access) by email and password'
            },
            'jwt-refresh': {
                'url': f'{url}{reverse_lazy("api:token_refresh")}',
                'info': 'generate jwt access token by refresh token'
            },
            'blog-categories': {
                'url': f'{url}{reverse_lazy("api:api-blog-category-list")}',
                'info': 'get all categories, create new category'
            },
        }, status=status.HTTP_200_OK)

