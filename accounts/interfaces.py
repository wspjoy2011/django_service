from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from accounts.dto import (
    ActivationTokenDTO,
    PasswordResetTokenDTO,
    UserWithProfileDTO,
    CustomUserDTO,
    ProfileDTO,
    TokenDTO,
    ReactivateUserTokenDTO,
    RequestPasswordResetTokenDTO,
    ResetPasswordTokenDTO
)


class AbstractUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> List[UserWithProfileDTO]:
        pass

    @abstractmethod
    def create(self, user_dto: CustomUserDTO, profile_dto: ProfileDTO) -> UserWithProfileDTO:
        pass

    @abstractmethod
    def create_activation_token_by_email(self, email: str, token: str) -> None:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserWithProfileDTO]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[UserWithProfileDTO]:
        pass

    @abstractmethod
    def get_activation_token_by_token_user_email(self, token: str, email: str) -> Optional[TokenDTO]:
        pass

    @abstractmethod
    def get_user_password_reset_token_by_user_email(self, email: str) -> Optional[PasswordResetTokenDTO]:
        pass

    @abstractmethod
    def get_user_activation_token_by_user_id(self, user_id: int) -> Optional[TokenDTO]:
        pass

    @abstractmethod
    def activate_user_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def update_user_password(self, user_id: int, new_password: str) -> None:
        pass

    @abstractmethod
    def delete_activation_token_by_id(self, token_id: int) -> None:
        pass

    @abstractmethod
    def delete_reset_password_token_by_id(self, token_id: int):
        pass

    @abstractmethod
    def create_password_reset_token(self, user_id: int, token: str) -> PasswordResetTokenDTO:
        pass


class UserServiceInterface(metaclass=ABCMeta):
    """Interface for UserService"""
    @abstractmethod
    def get_all_users(self) -> List[UserWithProfileDTO]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserWithProfileDTO | None:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserWithProfileDTO | None:
        pass

    @abstractmethod
    def create_user(self, user_dto: CustomUserDTO, profile_dto: ProfileDTO) -> UserWithProfileDTO:
        pass

    @abstractmethod
    def create_activation_token(self, user_dto: UserWithProfileDTO) -> ActivationTokenDTO:
        pass

    @abstractmethod
    def create_reactivation_token(self, reactivate_token_dto: ReactivateUserTokenDTO) -> ActivationTokenDTO:
        pass

    @abstractmethod
    def activate_user_with_token(self, activation_token_dto: ActivationTokenDTO) -> None:
        pass

    @abstractmethod
    def get_user_activate_token(self, activation_token_dto: ActivationTokenDTO) -> TokenDTO:
        pass

    @abstractmethod
    def get_activate_token_by_user_email(self, reactivate_token_dto: ReactivateUserTokenDTO) -> TokenDTO | None:
        pass

    @abstractmethod
    def create_password_reset_token(self, request_password_dto: RequestPasswordResetTokenDTO) -> PasswordResetTokenDTO:
        pass

    @abstractmethod
    def password_reset(self, password_reset_dto: ResetPasswordTokenDTO) -> None:
        pass

    @abstractmethod
    def verify_token_expiration(self, create_at: datetime) -> None:
        pass

    @abstractmethod
    def delete_activation_token(self, token: TokenDTO) -> None:
        pass


class RegisterEmailServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def send_activation_email(self, activation_token_dto: ActivationTokenDTO) -> None:
        pass

    @abstractmethod
    def send_password_reset_email(self, token: PasswordResetTokenDTO) -> None:
        pass
