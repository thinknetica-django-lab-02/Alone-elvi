from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from .models import Category, Contacts, Product, Size, Seller, Tag

from ckeditor.widgets import CKEditorWidget


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
admin.site.register(Category)
admin.site.register(Contacts)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Seller)
admin.site.register(Tag)
