from datetime import date

from django.core.exceptions import ValidationError


def validate_birth_date(birth_date):
    if birth_date.year < 1900:
        raise ValidationError('Invalid birth date - year must be greater than 1900.')
    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValidationError('You must be at least 18 years old to register.')
