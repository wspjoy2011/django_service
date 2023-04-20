from accounts.dto import (
    CustomUserDTO,
    ProfileDTO,
    UserWithProfileDTO,
    ActivationTokenDTO,
    ReactivateUserTokenDTO,
    RequestPasswordResetTokenDTO,
    ResetPasswordTokenDTO
)
from accounts.interfaces import RegisterEmailServiceInterface
from accounts.services import UserServiceInterface


class RegisterInteractor:
    """Interactor for registration new user and manage """
    def __init__(self, user_service: UserServiceInterface, email_service: RegisterEmailServiceInterface):
        self.user_service = user_service
        self.email_service = email_service

    def register_user(self, user_dto: CustomUserDTO, profile_dto: ProfileDTO) -> tuple[UserWithProfileDTO,
                                                                                       ActivationTokenDTO]:
        created_user = self.user_service.create_user(user_dto, profile_dto)
        activation_token_dto = self.user_service.create_activation_token(created_user)
        self.email_service.send_activation_email(activation_token_dto)
        return created_user, activation_token_dto

    def activate_user(self, activation_token_dto: ActivationTokenDTO) -> None:
        token = self.user_service.get_user_activate_token(activation_token_dto)
        self.user_service.verify_token_expiration(token.create_at)
        self.user_service.activate_user_with_token(activation_token_dto)
        self.user_service.delete_activation_token(token)

    def reactivate_user_token(self, reactivate_token_dto: ReactivateUserTokenDTO) -> ActivationTokenDTO:
        activation_token_dto = self.user_service.create_reactivation_token(reactivate_token_dto)
        self.email_service.send_activation_email(activation_token_dto)
        return activation_token_dto

    def request_password_reset(self, request_password_dto: RequestPasswordResetTokenDTO) -> None:
        token = self.user_service.create_password_reset_token(request_password_dto)
        self.email_service.send_password_reset_email(token)

    def password_reset(self, password_reset_dto: ResetPasswordTokenDTO) -> None:
        self.user_service.password_reset(password_reset_dto)

