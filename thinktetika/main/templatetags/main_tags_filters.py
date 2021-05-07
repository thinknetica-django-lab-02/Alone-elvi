from django import template
from django.utils import timezone
from django import template
import logging

from main.models import Category, Product

register = template.Library()
logger = logging.getLogger(__name__)

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
    logger.warning("thinktetika/main/templatetags/main_tags_filters.py")
    tags = Product.objects.get('tags').all()
    logger.warning("thinktetika/main/templatetags/main_tags_filters.py -> tags {}".format(tags))

    print(tags)
    request = context['request']
    return {'tags': tags, 'request': request}
