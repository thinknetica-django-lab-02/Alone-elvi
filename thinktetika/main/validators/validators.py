from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_age(value):
    age = relativedelta(timezone.now().date(), value).years
    if age < 18:
        raise ValidationError('Вам должно быть от 18 лет.')
