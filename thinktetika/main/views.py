from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView

from django.db.models.signals import post_save
from django.dispatch import receiver

from thinktetika.settings import DEFAULT_GROUP_NAME

from .email import email_template

from .tasks import sending_new_products_by_scheduler

import logging

from .forms import UserForm, ProfileForm
from .models import Product, Tag, Profile, Subscriber

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        """Метод ответсвенный за вывод главной страницы и отправку сообщений о новинках недели по расписанию."""
        context = super(IndexView, self).get_context_data(**kwargs)
        sending_new_products_by_scheduler()
        return context


def index(request):
    turn_on_block = True
    data = {'turn_on_block': turn_on_block, 'username': request.user.username}

    return render(request, "/", data)


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

    def post(self, request, *args, **kwargs):
        if request.POST.get('mailing'):
            mailing = request.POST.get('mailing')
            if mailing == 'subscribe':
                Subscriber.objects.create(user=request.user)
            elif mailing == 'unsubscribe':
                subscriber = Subscriber.objects.filter(user_id=request.user.pk).first()
                if subscriber:
                    subscriber.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class GoodsDetalView(DetailView):
    """класс GoodsDetalView выводит данные по единице товара из таблицы Product в шаблон good-detail.html"""
    model = Product
    template_name = 'pages/good-detail.html'
    success_url = '/goods/'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Класс ProfileUpdate используется в шаблоне pages/profile.html и доступно по адресу /accounts/profile/"""
    model = User
    form_class = UserForm
    template_name = 'pages/profile.html'
    success_url = '/accounts/profile/'

    def get_object(self, request):
        """Метод возвращает пользователя"""
        return request.user

    def get_context_data(self, **kwargs):
        """Метод получает и возвращает данные из формы"""
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):
        """Метод возвращает шаблон с переданным словарём для выполнения"""
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        """Метод проверки данных введённых в форме"""
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if not Group.objects.filter(name=DEFAULT_GROUP_NAME):
                Group.objects.get_or_create(name=DEFAULT_GROUP_NAME)
            instance.groups.add(Group.objects.get(name=DEFAULT_GROUP_NAME))
            Profile.objects.create(user=User.objects.get(username=instance))

            if instance.email:
                send_mail(
                    subject=email_template.subject,
                    message=email_template.message,
                    from_email=email_template.from_email,
                    recipient_list=[instance.email],
                    fail_silently=False,
                    html_message=email_template.html_message
                )

    def post(self, request, *args, **kwargs):
        """Метод возвращает шаблон с переданным словарём или ошибку заполнения формы"""
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


class CreateProduct(CreateView):
    """Класс CreateProduct, предназначен для создания нового товара"""
    model = Product
    template_name = 'pages/good-add.html'
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = '/goods/'


class UpdateProduct(UpdateView):
    """Класс UpdateProduct, предназначен для редактирования текущего товара"""
    model = Product
    template_name = 'pages/good-edit.html'
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/goods/'
