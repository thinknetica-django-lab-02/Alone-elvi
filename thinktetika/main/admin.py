from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.html import format_html

from django.db.models import QuerySet, Model
from django.http import HttpRequest

from main.models import Category, Contacts, Product, Size, Seller, Profile

admin.site.unregister(FlatPage)
admin.site.register(FlatPage)


class ArrayFieldListFilter(admin.SimpleListFilter):
    """
    Класс отвечающий за фильтрацию по тегам
    """

    title = 'Tags'
    parameter_name = 'tags'

    def lookups(self, request: HttpRequest, model_admin: Model):
        tags = Product.objects.values_list("tags", flat=True)
        tags = [(x, x) for sublist in tags for x in sublist if x]
        tags = sorted(set(tags))
        return tags

    def queryset(self, request: HttpRequest, queryset: QuerySet):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tags__contains=[lookup_value])
        return queryset


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = "__all__"


class FlatPageAdmin(FlatPageAdmin):
    form = FlatPageAdminForm


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = "Дата создания"


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_unpublished.short_description = "Не опубликовано"


def make_archive(modeladmin, request, queryset):
    queryset.update(is_archive=True)


make_archive.short_description = "Отправить в архив"


def make_unarchive(modeladmin, request, queryset):
    queryset.update(is_archive=False)


make_unarchive.short_description = "Убрать из архива"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс ProductAdmin определяет кастомизированное
    взаимодействие модели Product с админкой
    """
    actions = [make_published, make_unpublished, make_archive, make_unarchive]
    list_display = (
        "id",
        "title",
        "sku",
        "image",
        "size",
        "category",
        "weight",
        "quantity",
        "price",
        "seller",
        "pub_date",
        "creation_date",
        "is_archive",
        "is_published",
    )
    list_filter = (ArrayFieldListFilter, "pub_date", "category")
    readonly_fields = ("image",)
    search_fields = ("title", "description", "category",)
    list_editable = ("is_published", "is_archive",)
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        return format_html("<img src='{}' />".format(obj.image.url))

    get_image.short_description = "Изображение"


# class TagAdmin(admin.ModelAdmin):
#     list_display = ("title",)


admin.site.register(Category)
admin.site.register(Contacts)
admin.site.register(Size)
admin.site.register(Seller)


# admin.site.register(Tag)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_date")
