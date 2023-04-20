from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.schemas.auth import register_request_schema, register_response_schema, activate_user_request_schema, \
    activate_user_response_schema, reactivate_user_token_request_schema, reactivate_user_token_response_schema, \
    request_password_reset_token_request_schema, request_password_reset_token_response_schema, \
    reset_password_request_schema, reset_password_response_schema, token_obtain_pair_response_schema
from core.containers import ProjectContainer as UserContainer
from accounts.dto import (
    CustomUserDTO,
    ProfileDTO,
    ActivationTokenDTO,
    ReactivateUserTokenDTO,
    RequestPasswordResetTokenDTO,
    ResetPasswordTokenDTO
)
from api.serializers.auth import (
    CustomUserDTOSerializer,
    ProfileDTOSerializer,
    UserWithProfileDTOSerializer,
    ActivationTokenDTOSerializer,
    ReactivateUserTokenSerializer,
    RequestPasswordResetTokenSerializer,
    ResetPasswordTokenSerializer, CustomTokenObtainPairSerializer, TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer
)
from accounts.exceptions import (
    UserAlreadyExistsError,
    TokenExpiredError,
    InvalidTokenError,
    UserTokenNotFoundError,
    UserAlreadyActivatedError,
    UserNotFoundError,
    UserNotActivatedError, WeakPasswordError
)
from api.views.base import ApiBaseView


class JWTTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Generate JWT access and refresh tokens by email and password",
        request_body=CustomTokenObtainPairSerializer,
        responses={
            200: openapi.Response("JWT token pair", token_obtain_pair_response_schema)
        },
        tags=["JWT Auth"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class JWTTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Generate a new JWT access token using the refresh token",
        request_body=TokenRefreshSerializer,
        responses={
            200: openapi.Response("JWT token access", TokenRefreshResponseSerializer)
        },
        tags=["JWT Auth"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ApiRegisterView(APIView, ApiBaseView):
    """Register user with profile"""

    @swagger_auto_schema(
        operation_description="Register a new user with profile",
        request_body=register_request_schema,
        responses={
            201: register_response_schema,
            400: 'Bad Request',
        },
        tags=["auth"],
        security=[],
    )
    def post(self, request):
        user_serializer = CustomUserDTOSerializer(data=request.data)
        profile_serializer = ProfileDTOSerializer(data=request.data)

        user_serializer_is_valid = user_serializer.is_valid()
        profile_serializer_is_valid = profile_serializer.is_valid()

        if not (user_serializer_is_valid and profile_serializer_is_valid):
            return self._create_response_for_invalid_serializers(user_serializer, profile_serializer)

        user_dto = CustomUserDTO(**user_serializer.validated_data)
        profile_dto = ProfileDTO(**profile_serializer.validated_data)

        register_interactor = UserContainer.register_interactor()

        try:
            created_user, activation_token = register_interactor.register_user(user_dto, profile_dto)
        except UserAlreadyExistsError as exception:
            return self._create_response_for_exception(exception)

        return self._create_response_for_successful_registration(created_user, activation_token)

    def _create_response_for_successful_registration(self, created_user, activation_token):
        response = UserWithProfileDTOSerializer(created_user)
        return Response({
            "message": f"User registered successfully. Please check {created_user.email} for next instructions.",
            "token": activation_token.token,
            "user": response.data
        }, status=status.HTTP_201_CREATED)


class ApiActivateUserView(APIView, ApiBaseView):
    """Activate user with token by email"""

    @swagger_auto_schema(
        operation_description="Activate a user account",
        request_body=activate_user_request_schema,
        responses={
            200: activate_user_response_schema,
            400: 'Bad Request',
        },
        tags=["auth"],
        security=[],
    )
    def post(self, request):
        """
        Activate user account
        """
        token_serializer = ActivationTokenDTOSerializer(data=request.data)
        token_serializer_is_valid = token_serializer.is_valid()

        if not token_serializer_is_valid:
            return self._create_response_for_invalid_serializers(token_serializer)

        activation_token_dto = ActivationTokenDTO(**token_serializer.validated_data)
        register_interactor = UserContainer.register_interactor()

        try:
            register_interactor.activate_user(activation_token_dto)
        except (TokenExpiredError, UserTokenNotFoundError, UserAlreadyActivatedError, UserNotFoundError) as exception:
            return self._create_response_for_exception(exception)

        return self._create_response_for_successful_activation()

    def _create_response_for_successful_activation(self):
        return Response(
            {"message": "User account activated successfully."},
            status=status.HTTP_200_OK
        )


class ApiReactivateUserTokenView(APIView, ApiBaseView):
    """Create reactivation token"""

    @swagger_auto_schema(
        operation_description="Reactivate user activation token",
        request_body=reactivate_user_token_request_schema,
        responses={
            200: reactivate_user_token_response_schema,
            400: 'Bad Request',
        },
        tags=["auth"],
        security=[],
    )
    def post(self, request):
        """
        Reactivate user activation token
        """
        reactivate_token_serializer = ReactivateUserTokenSerializer(data=request.data)
        reactivate_token_serializer_is_valid = reactivate_token_serializer.is_valid()

        if not reactivate_token_serializer_is_valid:
            return self._create_response_for_invalid_serializers(reactivate_token_serializer)

        reactivate_token_dto = ReactivateUserTokenDTO(**reactivate_token_serializer.validated_data)
        register_interactor = UserContainer.register_interactor()

        try:
            activation_token = register_interactor.reactivate_user_token(reactivate_token_dto)
        except (UserNotFoundError, UserAlreadyActivatedError) as exception:
            return self._create_response_for_exception(exception)

        return self._create_response_for_successful_reactivation(activation_token)

    def _create_response_for_successful_reactivation(self, activation_token):
        return Response(
            {
                "message": "Reactivation token complete please check your email.",
                "token": activation_token.token,
            },
            status=status.HTTP_200_OK)


class ApiRequestPasswordResetView(APIView, ApiBaseView):
    """Create password reset token"""

    @swagger_auto_schema(
        operation_description="Request to create reset password token via email",
        request_body=request_password_reset_token_request_schema,
        responses={
            200: request_password_reset_token_response_schema,
            400: 'Bad Request',
        },
        tags=["auth"],
        security=[],
    )
    def post(self, request):
        """
        Request to create reset password token via email
        """
        password_reset_token_serializer = RequestPasswordResetTokenSerializer(data=request.data)
        password_reset_token_serializer_is_valid = password_reset_token_serializer.is_valid()

        if not password_reset_token_serializer_is_valid:
            return self._create_response_for_invalid_serializers(password_reset_token_serializer)

        password_reset_token_dto = RequestPasswordResetTokenDTO(**password_reset_token_serializer.validated_data)
        register_interactor = UserContainer.register_interactor()

        try:
            register_interactor.request_password_reset(password_reset_token_dto)
        except (UserNotFoundError, UserNotActivatedError) as exception:
            return self._create_response_for_exception(exception)

        return self._create_response_for_successful_reactivation()

    def _create_response_for_successful_reactivation(self):
        return Response(
            {
                "message": "Reset password token created please check your email."
            },
            status=status.HTTP_200_OK)


class ApiResetPasswordView(APIView, ApiBaseView):
    """Set new password using password reset token and email"""

    @swagger_auto_schema(
        operation_description="Reset user password",
        request_body=reset_password_request_schema,
        responses={
            200: reset_password_response_schema,
            400: 'Bad Request',
        },
        tags=["auth"],
        security=[],
    )
    def post(self, request):
        """
        Reset user password
        """
        password_reset_serializer = ResetPasswordTokenSerializer(data=request.data)
        password_reset_serializer_is_valid = password_reset_serializer.is_valid()

        if not password_reset_serializer_is_valid:
            return self._create_response_for_invalid_serializers(password_reset_serializer)

        password_reset_dto = ResetPasswordTokenDTO(**password_reset_serializer.validated_data)
        register_interactor = UserContainer.register_interactor()

        try:
            register_interactor.password_reset(password_reset_dto)
        except (UserNotFoundError, InvalidTokenError, TokenExpiredError, WeakPasswordError) as exception:
            return self._create_response_for_exception(exception)

        return self._create_response_for_successful_reactivation()

    def _create_response_for_successful_reactivation(self):
        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK)
