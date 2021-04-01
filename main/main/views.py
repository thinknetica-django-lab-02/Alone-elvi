from django.shortcuts import render


def index(request):
    turn_on_block = True
    data = {'turn_on_block': turn_on_block, 'username': request.user.username}

    return render(request, "pages/index.html", data)
