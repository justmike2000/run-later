from django.http import Http404
from django.shortcuts import render


def login(request):
    return render(request, 'login.htm', {})