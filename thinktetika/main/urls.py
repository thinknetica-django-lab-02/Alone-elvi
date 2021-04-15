"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from .validators.validators import group_check
from .views import GoodsListView, GoodsDetalView, CreateProduct, UpdateProduct, IndexView
from main.models import Product

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('goods/', GoodsListView.as_view(model=Product), name='goods'),
                  path('goods/<int:pk>/', GoodsDetalView.as_view(model=Product), name='good-detail'),
                  path('goods/add', group_check(CreateProduct.as_view()), name='good-add'),
                  path('goods/<int:pk>/edit', group_check(UpdateProduct.as_view()), name='good-edit'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
