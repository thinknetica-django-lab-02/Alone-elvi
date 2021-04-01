from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def server_current_time():
    """Получаем и передаём текущее время сервера"""
    return timezone.now()


@register.filter
def change_first_last_chars_in_string(string):
    """Меняем первый и последний символ строки местами"""
    return string[-1:] + string[1:-1] + string[:1]
