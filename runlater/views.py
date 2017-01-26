from django.http import Http404
from django.shortcuts import render


def login(request):
    return render(request, 'login.htm', {})


def error(request):
    return render(request, 'error.htm', {})


def verify_login(requst):
    return "DENIED!"