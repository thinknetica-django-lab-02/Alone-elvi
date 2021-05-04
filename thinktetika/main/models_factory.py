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
    logger.warning(
        "address - {}, phone - {}, email - {}, whatsapp - {}, telegram - {}, viber - {}, instagram - {} ".format(
            type(address), type(phone), type(email), type(whatsapp),
            type(telegram), type(viber), type(instagram)))


class SellerFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Seller"""

    class Meta:
        model = Seller

    title = FAKER.company()
    contacts = factory.SubFactory(ContactsFactory)

    logger.warning("Seller title - {}".format(type(title)))


class CategoryFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Category"""

    class Meta:
        model = Category

    title = FAKER.name()
    logger.warning("Category title - {}".format(type(title)))


class SizeFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Size"""

    class Meta:
        model = Size
        logger.warning(FAKER.country_code())

    size = FAKER.country_code()
    logger.warning("Size size - {}".format(type(size)))


class TagFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Tag"""

    class Meta:
        model = Tag
        django_get_or_create = ('title',)

    title = str(set([FAKER.word(), FAKER.word(), FAKER.word()]))
    logger.warning("Tag title - {}".format(title))


class ProductFactory(DjangoModelFactory):
    """Класс создающий рандомные данные для тестирования модели Product"""

    class Meta:
        model = Product
        django_get_or_create = ('title',)
        logger.warning("Product Meta")

    logger.warning("@factory.post_generation")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        logger.debug("extracted - {}".format(extracted))

        if not create:
            logger.warning("extracted - {}".format(extracted))
            return
        if extracted:
            logger.warning("extracted - {}".format(extracted))
            for _ in extracted:
                logger.warning("extracted - {}".format(extracted))
                self.tags.add('TagFactory()')

        else:
            logger.warning("extracted - {}".format(extracted))
            tags = TagFactory()
            self.tags.add(tags)

    logger.warning("@factory.post_generation")

    title = FAKER.name()
    sku = FAKER.country_code() + str(FAKER.random_digit())
    image = FAKER.image_url()
    size = factory.SubFactory(SizeFactory)
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)

    weight = FAKER.numerify()
    quantity = FAKER.numerify()
    price = FAKER.numerify()

    logger.warning(
        "title - {}, sku - {} image - {}, weight - {}, quantity - {}, price - {}, tags - {}".format(
            type(title), type(sku), type(image), weight, quantity, price, tags))
