from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'page404.html')


def internal_server_error(requset):
    return render(request, 'page500.html')


