from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.models import Account
from jobs.models import Job


def index(request):
    return render(request, 'index.htm', {})


@login_required(login_url="/login_user/")
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

    return render(request, 'jobs.htm', {'model': 'jobs',
                                        'search_term': search,
                                        'max_pages': settings.MAX_PAGES,
                                        'current_page': page})


@login_required(login_url="/login_user/")
def add_job(request):
    org = Account.objects.get(user=request.user).organization
    job = Job.objects.create(organization=org)
    return render(request, 'job_details.htm', {'job': job})


@login_required(login_url="/login_user/")
def job_detail(request, num):
    try:
        job = Job.objects.get(pk=num)
    except Job.DoesNotExist:
        return render(request, 'error.htm', {"message": "Job does not exist!"})
    return render(request, 'job_details.htm', {'job': job})


def build_save_dict(request, field):
    value = request.POST.get(field, None)
    if value is not None:
        return {field: value}
    return {}


@login_required(login_url="/login_user/")
def job(request, num):
    if request.method == "GET":
        return job_detail(request, num)
    elif request.method == "POST":
        update_dict = {}
        update_dict.update(build_save_dict(request, 'command'))
        update_dict.update(build_save_dict(request, 'action'))
        update_dict.update(build_save_dict(request, 'path'))
        update_dict.update(build_save_dict(request, 'parameters'))
        print update_dict
        Job.objects.filter(pk=num).update(**update_dict)
        return job_detail(request, num)
    elif request.method == "DELETE":
        try:
            Job.objects.get(pk=num).delete()
        except Job.DoesNotExist:
            pass
        return HttpResponseRedirect("/dashboard/jobs/")
    else:
        return render(request, 'error.htm', {"message": "Method not allowed."}, status=405)



@login_required(login_url="/login_user/")
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
