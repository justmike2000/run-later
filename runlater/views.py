from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.models import Account


def index(request):
    return render(request, 'index.htm', {})


@login_required(login_url="/login/")
def jobs(request):
    org = Account.objects.get(user=request.user).organization

    if request.method == "POST":
        page = int(request.POST.get('page', 1))
        search = request.POST.get('search', '')
    else:
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search', '')

    if not org:
        return render(request, 'dashboard.htm', {})

    return render(request, 'jobs.htm', {'search_term': search,
                                        'max_pages': settings.MAX_PAGES,
                                        'current_page': page})


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'dashboard.htm', {})


def login_user(request):
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect("/dashboard/")


    return render(request, 'login.htm', {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


@require_http_methods(["POST"])
def verify_login(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return HttpResponseRedirect("/dashboard/")
    else:
        return render(request, 'error.htm', {"message": "Invalid credentials"})
