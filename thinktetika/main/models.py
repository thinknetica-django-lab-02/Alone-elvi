from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils import timezone

from phone_field import PhoneField

from .validators.validators import validate_age

from .email import new_product_email_template


class Contacts(models.Model):
    """Класс Contacts
    Предназначен для хранения контактов
    Может быть связан по связанному полю contacts с классом  Seller.
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
        """ Выводит при запросе адрес, телефон и электронную почту"""
        return self.address + ' ' + self.phone + ' ' + self.email

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Size(models.Model):
    """Класс Size
    Класс предназначен для хранения данных размеров, связан по полю size в классе Product
    """
    size = models.CharField('Размер', max_length=6, default='')

    def __str__(self):
        """Метод возвращает запрашиваемый размер"""
        return self.size

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Category(models.Model):
    """Класс Cateory используется для храниения категорий товаров,
    может быть связан с классом Product по полю category."""
    title = models.CharField('Название', max_length=150, default='')

    def __str__(self):
        """Метод возвращает название запрашиваемой категории."""
        return self.title

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Seller(models.Model):
    """Класс Seller хранит данные о продавце,
     связан с классом Contacts по полю contacts.
     Используется классе Product по связанному полю seller, которое не может быть пустым."""
    title = models.CharField('Название', max_length=150, default='')
    contacts = models.ForeignKey('Contacts', on_delete=models.CASCADE)

    def __str__(self):
        """Метод возвращает название запрашиваемого продавца."""
        return self.title

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Product(models.Model):
    """
    Класс Product используется для хранения данных по товару.
    Может быть связан с классами Category, Product, Size,
    Tag, Seller по полям совпадающими с именами классов.
    """
    title = models.CharField('Название', max_length=150, default='')
    description = models.CharField('Описание', max_length=250, default='')
    sku = models.CharField('Артикул', max_length=20, default='')
    image = models.ImageField('Изображение', upload_to='products/', null=True,
                              blank=True)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    tags = ArrayField(models.CharField(max_length=50, blank=True), default=list,
                      size=8, blank=True)

    weight = models.DecimalField('Вес', max_digits=10, decimal_places=2)
    quantity = models.DecimalField('Количество', max_digits=10,
                                   decimal_places=2)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, null=False)
    pub_date = models.DateTimeField('Дата заполнения', default=timezone.now,
                                    blank=True)
    creation_date = models.DateTimeField('Дата создания', default=timezone.now,
                                         blank=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    is_archive = models.BooleanField('Архивный', default=False)
    browsing_count = models.IntegerField('Просмотры кол-во', default=0)

    def __str__(self):
        """Метод возвращает название запрашиваемого товара."""
        return f"{self.title} - {self.category} - {self.tags}"

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return f'/goods/{self.pk}/'


class ProductBrowsing(models.Model):
    """
    Класс представления отчета просмотра отдельных записей товаров
    """
    title = models.CharField('Наименование', max_length=150, unique=True)
    sku = models.CharField('Артикул', max_length=20, default='')
    image = models.ImageField('Изображение', upload_to='products/', null=True,
                              blank=True)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'product_browsing'


class Profile(models.Model):
    """Класс Profile используется для работы с профилями пользователей"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField('Дата рождения', validators=[validate_age],
                                  default=timezone.now().date())
    avatar = models.ImageField('Аватар', upload_to='avatars/', null=True,
                               blank=True)
    phone_number = PhoneField('Номер телефона', blank=True)
    phone_confirmed = models.PositiveIntegerField('Подтверждено',
                                                  default=0000)

    def __str__(self):
        """Метод возвращает имя пользователя"""
        return f"{self.user.username}"

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SMSConfirm(models.Model):
    """
    Класс подтверждающий SMS код
    """
    code = models.PositiveIntegerField('Код подтверждения')
    status = models.CharField('Статус ответа сервера', max_length=14)
    user = models.ManyToManyField(User)


class Subscriber(models.Model):
    """
    Класс Subscriber используется для отправки
    рассылки пользователям подписанным на неё
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="subscriber")

    class Meta:
        """Класс формирующий название в единственном и множественном числах"""
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        """Метод возвращает имя пользователя"""
        return self.user.username


def sending_html_mail(subject, text_content, html_content, from_email, to_list):
    message = EmailMultiAlternatives(subject, text_content, from_email, to_list)
    message.attach_alternative(html_content, "text/html")
    message.send()


@receiver(post_save, sender=Product)
def get_subscriber(sender, instance, created, **kwargs):
    if created:
        emails = [e.user.email for e in Subscriber.objects.all()]
        subject = new_product_email_template.subject + {instance.title}
        text_content = new_product_email_template.text_content + {
            instance.title} + new_product_email_template.text_content_url + {
                           instance.get_absolute_url()}
    html_content = f'''
            <ul>
                <li>Название: {instance.title}</li>
                <li>Цена: {instance.price}</li>
            </ul>
            Подробности можно получить по 
            <a href="{instance.get_absolute_url()}">ссылке</a>.
        '''
    from_email = new_product_email_template.from_email
    sending_html_mail(subject, text_content, html_content, from_email, emails)
