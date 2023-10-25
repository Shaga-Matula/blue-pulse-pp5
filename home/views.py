from django.shortcuts import render


def index(request):
    """ Render home/index.html"""
    return render(request, 'home/index.html')
