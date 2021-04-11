from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.utils import timezone
from main.settings import SELLERS_GROUP


def validate_age(value):
    age = relativedelta(timezone.now().date(), value).years
    if age < 18:
        raise ValidationError('Вам должно быть от 18 лет.')


def group_check(function):
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated and u.groups.filter(name=SELLERS_GROUP)) or u.is_superuser,
        redirect_field_name=''
    )
    return actual_decorator(function)
