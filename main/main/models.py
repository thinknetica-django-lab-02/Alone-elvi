from django.db import models


class Contacts(models.Model):
    address = models.CharField('Адрес', max_length=150, default='')
    phone = models.CharField('Телефон', max_length=12, default='')
    email = models.CharField('E-mail', max_length=100, default='')
    whatsapp = models.CharField('WhatsApp', max_length=12, default='')
    telegram = models.CharField('Telegram', max_length=12, default='')
    viber = models.CharField('Viber', max_length=12, default='')
    instagram = models.CharField('Instagram', max_length=50, default='')
    map = models.CharField('Карта', max_length=250, default='')

    def __str__(self):
        return self.address + ' ' + self.phone + ' ' + self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Size(models.Model):
    size = models.CharField('Размер', max_length=6, default='')

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Category(models.Model):
    title = models.CharField('Название', max_length=150, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField('Название', max_length=50, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Seller(models.Model):
    title = models.CharField('Название', max_length=150, default='')
    contacts = models.ForeignKey('Contacts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Product(models.Model):
    title = models.CharField('Название', max_length=150, default='')
    sku = models.CharField('Артикул', max_length=20, default='')
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    weight = models.DecimalField('Вес', max_digits=10, decimal_places=2)
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=2)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
