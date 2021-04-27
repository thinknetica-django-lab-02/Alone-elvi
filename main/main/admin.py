from django.contrib import admin

from main.models import Category, Contacts, Product, Size, Seller, Tag, \
    Subscriber, Profile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Subscriber)
admin.site.register(Contacts)
admin.site.register(Size)
admin.site.register(Seller)
