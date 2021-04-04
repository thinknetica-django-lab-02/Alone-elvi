from django import template
from django.utils import timezone
from django import template

from main.models import Category, Tag

register = template.Library()


@register.simple_tag
def server_current_time():
    """Получаем и передаём текущее время сервера"""
    return timezone.now()


@register.filter
def change_first_last_chars_in_string(string):
    """Меняем первый и последний символ строки местами"""
    return string[-1:] + string[1:-1] + string[:1]


@register.inclusion_tag('main/snippets/tags_links.html', takes_context=True)
def goods_tags_links(context) -> dict:
    """Возвращает список ссылок <a> на тэги товаров"""
    tags = Tag.objects.all()
    print(tags)
    request = context['request']
    return {'tags': tags, 'request': request}