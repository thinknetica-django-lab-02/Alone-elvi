import logging

import factory
from faker.factory import Factory

from factory.django import DjangoModelFactory

from .models import Product, Seller, Contacts, Size, Tag, Category

logger = logging.getLogger(__name__)

FAKER = Factory.create('ru_RU')


class ContactsFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Contacts"""

    class Meta:
        model = Contacts

    address = FAKER.address()
    phone = FAKER.phone_number()
    email = FAKER.email()
    whatsapp = FAKER.phone_number()
    telegram = FAKER.phone_number()
    viber = FAKER.phone_number()
    instagram = FAKER.phone_number()


class SellerFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Seller"""

    class Meta:
        model = Seller

    title = FAKER.company()
    contacts = factory.SubFactory(ContactsFactory)


class CategoryFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Category"""

    class Meta:
        model = Category

    title = FAKER.word()


class SizeFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Size"""

    class Meta:
        model = Size

    size = FAKER.country_code() + str(FAKER.random_digit())


class TagFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Tag"""

    class Meta:
        model = Tag
        django_get_or_create = ('title',)

    title = FAKER.word()


class ProductFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Product"""

    class Meta:
        model = Product

    title = FAKER.word()
    sku = FAKER.country_code() + str(FAKER.random_digit())
    image = FAKER.image_url()
    size = factory.SubFactory(SizeFactory)
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)

    weight = FAKER.random_digit()
    quantity = FAKER.random_digit()
    price = FAKER.random_digit()

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return
        if extracted:
            for _ in extracted:
                self.tags.add(TagFactory())
        else:
            tags = TagFactory()
            self.tags.add(tags)
