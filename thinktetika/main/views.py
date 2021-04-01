from time import timezone

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

def index(request):
    turn_on_block = True
    data = {'turn_on_block': turn_on_block, 'username': request.user.username}

    return render(request, "pages/index.html", data)

class GoodsListView(ListView):
    model = Product
    template_name = 'pages/goods.html'

class GoodsDetalView(DetailView):
    model = Product
    template_name = 'pages/good-detail.html'

