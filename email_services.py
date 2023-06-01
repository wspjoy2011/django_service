import json
from celery import shared_task
from django.core.mail import send_mail

from accounts.dto import ActivationTokenDTO, PasswordResetTokenDTO
from accounts.interfaces import RegisterEmailServiceInterface


@shared_task
def _send_email_async(subject, message, from_email, recipient_list, **kwargs):
    send_mail(subject, message, from_email, recipient_list, **kwargs)


class RegisterEmailService(RegisterEmailServiceInterface):
    def send_activation_email(self, activation_token_dto: ActivationTokenDTO) -> None:
        activation_json = {
            'token': activation_token_dto.token,
            'email': activation_token_dto.email
        }
        _send_email_async.delay(
            'Activate your account',
            f'Send this json to activate your account: {json.dumps(activation_json)}',
            'noreply@example.com',
            [activation_token_dto.email],
            fail_silently=False,
        )

    def send_password_reset_email(self, token: PasswordResetTokenDTO) -> None:
        password_reset_json = {
            'password_reset_token': token.token,
            'email': token.email,
            'new_password': 'your_new_password'
        }
        _send_email_async.delay(
            'Password Reset',
            f'Please follow this link to reset your password: {json.dumps(password_reset_json)}',
            'noreply@example.com',
            [token.email],
            fail_silently=False,
        )
