from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .forms import UserForm, ProfileForm
from .models import Product, Tag



def index(request):
    turn_on_block = True
    data = {'turn_on_block': turn_on_block, 'username': request.user.username}

    return render(request, "pages/index.html", data)


class GoodsListView(ListView):
<<<<<<< HEAD
    """Класс GoodsListView генерирует список товаров в шаблон pages/goods.html"""
||||||| 34ba96f
=======
    """класс GoodsListView выводит список товаров из таблицы Product в шаблон pages/goods.html
        с разбивкой по 10 товаров на страницу
    """
>>>>>>> main
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
<<<<<<< HEAD
    """Класс GoodsListView генерирует описание единицы товара в шаблон pages/good-detail.html"""
||||||| 34ba96f
=======
    """класс GoodsDetalView выводит данные по единице товара из таблицы Product в шаблон good-detail.html"""
>>>>>>> main
    model = Product
    template_name = 'pages/good-detail.html'
<<<<<<< HEAD
    success_url = '/goods/'
||||||| 4710e6f
=======
<<<<<<< HEAD
||||||| 34ba96f

=======
>>>>>>> main


class ProfileUpdate(UpdateView):
    """Класс ProfileUpdate используется в шаблоне pages/profile.html и доступно по адресу /accounts/profile/"""
    model = User
    form_class = UserForm
    template_name = 'pages/profile.html'
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        """Метод получения и возврата данных из queryset"""
        return super(ProfileUpdate, self).get_queryset().get()

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

    def post(self, request, *args, **kwargs):
        """Метод возвращает шаблон с переданным словарём или ошибку заполнения формы"""
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return render(request, self.template_name, {'form': form, 'profile_form': profile_form})
        else:
            return self.form_invalid(form)
<<<<<<< HEAD


class CreateProduct(CreateView):
    """Класс CreateProduct, предназначен для создания нового товара"""
    model = Product
    template_name = 'pages/good-add.html'
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = '/goods/'


class UpdateProduct(UpdateView):
    """Класс UpdateProduct, предназначен для редактирования текщего товара"""
    model = Product
    template_name = 'pages/good-edit.html'
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/goods/'
||||||| 4710e6f
=======
>>>>>>> main
>>>>>>> main
