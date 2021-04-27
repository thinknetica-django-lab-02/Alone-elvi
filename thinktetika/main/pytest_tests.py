import pytest
from django.urls import reverse

from main.models import *


@pytest.mark.django_db
def MainPageViewTests(client):
    """
    Метод проверяет код ответа сервера.
    """
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def GoodsListViewTests(client):
        """
        Метод проверяет код ответа сервера.
        """
        response = client.get(reverse('goods'))
        assert response.status_code == 200

@pytest.mark.django_db
def GoodViewTests(client):
    """
    Метод проверяет код ответа сервера.
    """
    goods = Product.objects.all()
    for good in goods:
        response = client.get(reverse('good-detail/' + good.pk))
        assert response.status_code == 200


