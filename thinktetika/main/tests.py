from django.test import TestCase
from django.urls import reverse
from main.models import *



class MainPageViewTests(TestCase):
    def test_response_view(self):
        """
        Метод проверяет код ответа сервера.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


#
class GoodsListViewTests(TestCase):
    def test_response_view(self):
        """
        Метод проверяет код ответа сервера.
        """
        response = self.client.get(reverse('goods'))
        self.assertEqual(response.status_code, 200)


class GoodViewTests(TestCase):
    def test_response_view(self):
        """
        Метод проверяет код ответа сервера.
        """
        goods = Product.objects.all()
        for good in goods:
            response = self.client.get(reverse('good-detail/' + good.pk))
            self.assertEqual(response.status_code, 200)
