import json
import threading

from django.core.mail import send_mail

from accounts.dto import ActivationTokenDTO, PasswordResetTokenDTO
from accounts.interfaces import RegisterEmailServiceInterface


class RegisterEmailService(RegisterEmailServiceInterface):
    def _send_email_async(self, subject, message, from_email, recipient_list, **kwargs):
        thread = threading.Thread(
            target=send_mail,
            args=(subject, message, from_email, recipient_list),
            kwargs=kwargs)
        thread.start()

    def send_activation_email(self, activation_token_dto: ActivationTokenDTO) -> None:
        activation_json = {
            'token': activation_token_dto.token,
            'email': activation_token_dto.email
        }
        self._send_email_async(
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
        self._send_email_async(
            'Password Reset',
            f'Please follow this link to reset your password: {json.dumps(password_reset_json)}',
            'noreply@example.com',
            [token.email],
            fail_silently=False,
        )
