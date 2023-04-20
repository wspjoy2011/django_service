from typing import List, Optional

from annoying.functions import get_object_or_None
from django.db import transaction

from .interfaces import AbstractUserRepository
from .models import CustomUser, Profile, ActivationToken, PasswordResetToken
from .dto import CustomUserDTO, ProfileDTO, UserWithProfileDTO, TokenDTO, PasswordResetTokenDTO


class UserRepository(AbstractUserRepository):
    def get_all(self) -> List[UserWithProfileDTO]:
        return CustomUser.objects.all()

    def create(self, user_dto: CustomUserDTO, profile_dto: ProfileDTO) -> UserWithProfileDTO:
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=user_dto.email,
                username=user_dto.username,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                password=user_dto.password,
                is_active=False
            )
            Profile.objects.create(
                user=user,
                avatar=profile_dto.avatar,
                gender=profile_dto.gender,
                date_of_birth=profile_dto.date_of_birth,
                bio=profile_dto.bio,
                info=profile_dto.info
            )
        return self._user_with_profile_dto(user)

    def create_activation_token_by_email(self, email: str, token: str) -> None:
        new_user = CustomUser.objects.get(email=email)
        ActivationToken.objects.create(user=new_user, token=token)

    def get_user_by_email(self, email: str) -> Optional[UserWithProfileDTO]:
        user = get_object_or_None(CustomUser, email=email)
        return self._user_with_profile_dto(user) if user else None

    def get_user_by_username(self, username: str) -> Optional[UserWithProfileDTO]:
        user = get_object_or_None(CustomUser, username=username)
        return self._user_with_profile_dto(user) if user else None

    def get_user_activation_token_by_user_id(self, user_id: int) -> TokenDTO | None:
        user = CustomUser.objects.get(id=user_id)
        activation_token = get_object_or_None(ActivationToken, user=user)
        return self._activation_token_dto(activation_token) if activation_token else None

    def get_activation_token_by_token_user_email(self, token: str, email: str) -> TokenDTO | None:
        activation_token = get_object_or_None(ActivationToken, token=token, user__email=email)
        return self._activation_token_dto(activation_token) if activation_token else None

    def get_user_password_reset_token_by_user_email(self, email: str) -> PasswordResetTokenDTO | None:
        password_reset_token = get_object_or_None(PasswordResetToken,  user__email=email)
        return self._password_reset_token_dto(password_reset_token) if password_reset_token else None

    def activate_user_by_email(self, email: str) -> bool:
        user = CustomUser.objects.get(email=email)
        if not user.is_active:
            user.is_active = True
            user.save()
            return True
        return False

    @transaction.atomic()
    def delete_activation_token_by_id(self, token_id: int) -> None:
        token = ActivationToken.objects.get(pk=token_id)
        token.delete()

    @transaction.atomic()
    def delete_reset_password_token_by_id(self, token_id: int):
        token = PasswordResetToken.objects.get(pk=token_id)
        token.delete()

    def create_password_reset_token(self, user_id: int, token: str) -> PasswordResetTokenDTO:
        user = CustomUser.objects.get(id=user_id)
        reset_password_token = PasswordResetToken.objects.create(user=user, token=token)
        return self._password_reset_token_dto(reset_password_token)

    def update_user_password(self, user_id: int, new_password: str) -> None:
        user = CustomUser.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()

    def _user_with_profile_dto(self, user: CustomUser) -> UserWithProfileDTO:
        profile = user.profile
        return UserWithProfileDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            profile=ProfileDTO(
                avatar=profile.avatar,
                gender=profile.gender,
                date_of_birth=profile.date_of_birth,
                bio=profile.bio,
                info=profile.info
            )
        )

    def _activation_token_dto(self, activation_token: ActivationToken) -> TokenDTO:
        return TokenDTO(
            id=activation_token.pk,
            token=activation_token.token,
            create_at=activation_token.created_at
        )

    def _password_reset_token_dto(self, reset_password_token: PasswordResetToken) -> PasswordResetTokenDTO:
        return PasswordResetTokenDTO(
            id=reset_password_token.pk,
            token=reset_password_token.token,
            email=reset_password_token.user.email,
            create_at=reset_password_token.created_at,
        )
