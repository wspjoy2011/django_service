import re
import secrets
from datetime import datetime
from django.utils import timezone
from typing import List

from .interfaces import UserServiceInterface
from .repositories import AbstractUserRepository
from .dto import (
    CustomUserDTO,
    ProfileDTO,
    UserWithProfileDTO,
    ActivationTokenDTO,
    TokenDTO,
    ReactivateUserTokenDTO,
    RequestPasswordResetTokenDTO,
    PasswordResetTokenDTO,
    ResetPasswordTokenDTO
)
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    UserTokenNotFoundError,
    UserAlreadyActivatedError,
    TokenExpiredError,
    UserNotActivatedError,
    InvalidTokenError,
    WeakPasswordError
)


class UserService(UserServiceInterface):
    """Service layer to work with user domain logic"""
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def get_all_users(self) -> List[UserWithProfileDTO]:
        """Get all user from repository"""
        return self.repository.get_all()

    def get_user_by_username(self, username: str) -> UserWithProfileDTO | None:
        """Get user by username"""
        return self.repository.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> UserWithProfileDTO | None:
        """Get user by email"""
        return self.repository.get_user_by_email(email)

    def create_user(self, user_dto: CustomUserDTO, profile_dto: ProfileDTO) -> UserWithProfileDTO:
        """Create new user"""
        if self.repository.get_user_by_email(user_dto.email) or self.repository.get_user_by_username(user_dto.username):
            raise UserAlreadyExistsError()

        return self.repository.create(user_dto, profile_dto)

    def create_activation_token(self, user_dto: UserWithProfileDTO) -> ActivationTokenDTO:
        """Generate and create activation token"""
        token = self._generate_token()
        activation_token_dto = ActivationTokenDTO(email=user_dto.email, token=token)
        self.repository.create_activation_token_by_email(activation_token_dto.email, activation_token_dto.token)
        return activation_token_dto

    def get_user_activate_token(self, activation_token_dto: ActivationTokenDTO) -> TokenDTO:
        """Check if user activation token exists"""
        self._get_user_by_email_or_raise(activation_token_dto.email)

        token_dto = self.repository.get_activation_token_by_token_user_email(activation_token_dto.token,
                                                                             activation_token_dto.email)
        if not token_dto:
            raise UserTokenNotFoundError()
        return token_dto

    def get_activate_token_by_user_email(self, reactivate_token_dto: ReactivateUserTokenDTO) -> TokenDTO | None:
        """Get exists activation token by user email"""
        user_dto = self._get_user_by_email_or_raise(reactivate_token_dto.email)
        user_token = self.repository.get_user_activation_token_by_user_id(user_dto.id)
        return user_token

    def activate_user_with_token(self, activation_token_dto: ActivationTokenDTO) -> None:
        """Activate user with token"""
        activate_status = self.repository.activate_user_by_email(activation_token_dto.email)
        if not activate_status:
            raise UserAlreadyActivatedError()

    def create_reactivation_token(self, reactivate_token_dto: ReactivateUserTokenDTO) -> ActivationTokenDTO:
        """Delete old token if exists, check if user is already activated, create new token"""
        old_token = self.get_activate_token_by_user_email(reactivate_token_dto)
        if old_token:
            self.delete_activation_token(old_token)

        user = self.get_user_by_email(reactivate_token_dto.email)
        if user.is_active:
            raise UserAlreadyActivatedError()

        activation_token_dto = self.create_activation_token(user)
        return activation_token_dto

    def delete_activation_token(self, token: TokenDTO) -> None:
        """Delete activation token"""
        self.repository.delete_activation_token_by_id(token.id)

    def create_password_reset_token(self, request_password_dto: RequestPasswordResetTokenDTO) -> PasswordResetTokenDTO:
        user = self._get_user_by_email_or_raise(request_password_dto.email)
        if not user.is_active:
            raise UserNotActivatedError()

        old_password_reset_token = self.repository.get_user_password_reset_token_by_user_email(
            request_password_dto.email)
        if old_password_reset_token:
            self.repository.delete_reset_password_token_by_id(old_password_reset_token.id)

        token = self._generate_token(64)
        reset_password_token = self.repository.create_password_reset_token(user.id, token)
        return reset_password_token

    def password_reset(self, password_reset_dto: ResetPasswordTokenDTO) -> None:
        """Reset user password by  reset token"""
        user = self._get_user_by_email_or_raise(password_reset_dto.email)
        token = self.repository.get_user_password_reset_token_by_user_email(user.email)
        if token.token != password_reset_dto.token:
            raise InvalidTokenError()

        self.verify_token_expiration(token.create_at)
        self._validate_password(password_reset_dto.new_password)
        self.repository.update_user_password(user.id, password_reset_dto.new_password)
        self.repository.delete_reset_password_token_by_id(token.id)

    def verify_token_expiration(self, create_at: datetime):
        """Verify token expiration"""
        if timezone.localtime(create_at) < timezone.now() - timezone.timedelta(days=1):
            raise TokenExpiredError()

    def _validate_password(self, password: str) -> None:
        if len(password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Za-z]", password):
            raise WeakPasswordError("Password must contain at least one letter.")

        if not re.search(r"\d", password):
            raise WeakPasswordError("Password must contain at least one digit.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise WeakPasswordError("Password must contain at least one special character.")

    def _generate_token(self, length: int = 32) -> str:
        """Generate activation token"""
        return secrets.token_hex(length // 2)

    def _get_user_by_email_or_raise(self, email: str) -> UserWithProfileDTO:
        """Get user by email or raise error"""
        user_dto = self.repository.get_user_by_email(email)
        if not user_dto:
            raise UserNotFoundError()
        return user_dto
