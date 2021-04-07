from time import timezone
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Tag


def index(request):
    turn_on_block = True
    data = {'turn_on_block': turn_on_block, 'username': request.user.username}

    return render(request, "pages/index.html", data)


class GoodsListView(ListView):
    """класс GoodsListView выводит список товаров из таблицы Product в шаблон pages/goods.html
        с разбивкой по 10 товаров на страницу
    """
    model = Product
    template_name = 'pages/goods.html'
    paginate_by = 10

    def get_queryset(self):
        """Получаем и передаём данные по товарам отфильтрованные по полю tags, если оно не пустое.
        Если пустое передаём все товары"""
        queryset = super(GoodsListView, self).get_queryset()
        tag = self.request.GET.get("tag")
        if tag is not None:
            return queryset.filter(tags__title=tag).order_by("id")
        return queryset

    def get_context_data(self, **kwargs):
        """Получаем список тегов и передаём в адресную строку браузера часть запроса содержащий необходимый тег."""
        context = super(GoodsListView, self).get_context_data(**kwargs)
        context["tags_list"] = Tag.objects.all()
        tag = self.request.GET.get("tag")
        if tag:
            context["tags_url"] = "tag={}&".format(tag)
        return context


class GoodsDetalView(DetailView):
    """класс GoodsDetalView выводит данные по единице товара из таблицы Product в шаблон good-detail.html"""
    model = Product
    template_name = 'pages/good-detail.html'
