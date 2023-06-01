from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)

