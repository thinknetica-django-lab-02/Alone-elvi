from time import timezone
import logging
from django import forms
from django.shortcuts import get_object_or_404, redirect

logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from .models import Product, Tag, Profile
from .forms import ProfileForm
from django.contrib import messages


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


class ProfileUpdate(UpdateView):
    """Класс ProfileUpdate используется в шаблоне pages/profile.html и доступно по адресу /accounts/profile/"""
    model = Profile
    form_class = ProfileForm
    template_name = 'pages/profile.html'

    def get_object(self, queryset=None):
        return super(ProfileUpdate, self).get_queryset().get()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Профиль пользователя был обновлён")
        return redirect('profile-update')
