from django.db import models


class Contacts(models.Model):
    """Класс Contacts
        Предназначен для хранения контактов
        Может быть связан по связанному полю сontacts с классом  Seller.
    """
    address = models.CharField('Адрес', max_length=150, default='')
    phone = models.CharField('Телефон', max_length=12, default='')
    email = models.CharField('E-mail', max_length=100, default='')
    whatsapp = models.CharField('WhatsApp', max_length=12, default='')
    telegram = models.CharField('Telegram', max_length=12, default='')
    viber = models.CharField('Viber', max_length=12, default='')
    instagram = models.CharField('Instagram', max_length=50, default='')
    map = models.CharField('Карта', max_length=250, default='')

    def __str__(self):
        """ Выводит при запросе адрес, телефон и элетронную почту"""
        return self.address + ' ' + self.phone + ' ' + self.email

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Size(models.Model):
    """Класс Size
    Класс преданзначен для хранения данных размеров, связан по полю size в классе Product
    """
    size = models.CharField('Размер', max_length=6, default='')

    def __str__(self):
        """Метод возвращает запрашиваемый размер"""
        return self.size

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Category(models.Model):
    """Класс Cateory используется для храниения категорий товаров, может быть связан с классом Product по полю category."""
    title = models.CharField('Название', max_length=150, default='')

    def __str__(self):
        """Метод возвращает название запрашиваемой категории."""
        return self.title

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    """Класс Tag, хранит тэги товара.
    Может быть связан с классом Product по полю tag с отношением многие ко многим.
    """
    title = models.CharField('Название', max_length=50, default='')

    def __str__(self):
        """Метод возвращает название запрашивамого тега."""
        return self.title

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Seller(models.Model):
    """Класс Seller хранит данные о продавце,
    связан с классом Contacts по полю contacts.
    Предполагается использовать в классе Product по связанному полю seller, которое не может быть пустым."""
    title = models.CharField('Название', max_length=150, default='')
    contacts = models.ForeignKey('Contacts', on_delete=models.CASCADE)

    def __str__(self):
        """Метод возвращает название запрашивамого продавца."""
        return self.title

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Product(models.Model):
    """Класс Product используется для храниния данных по товару.
    Может быть связан с классами Category, Product, Size, Tag по полям совпадающими с именами классов.
    """
    title = models.CharField('Название', max_length=150, default='')
    sku = models.CharField('Артикул', max_length=20, default='')
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    weight = models.DecimalField('Вес', max_digits=10, decimal_places=2)
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=2)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)

    def __str__(self):
        """Метод возвращает название запрашивамого товара."""
        return self.title

    class Meta:
        """Класс формируюший название в единственном и множественном числах"""
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
