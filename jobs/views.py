from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.conf import settings
from django.db.models import Q

import math
import decimal

from runlater.utils import paginate_objects
from accounts.models import Account
from jobs.models import Job, Run


@csrf_exempt
@require_http_methods(["POST", "GET"])
@login_required(login_url="/login_user/")
def jobs(request):
    try:
        org = Account.objects.get(user=request.user).organization
    except Account.DoesNotExist:
        return HttpResponse("[]")

    if request.method == "POST":
        items_per_page = request.POST.get('items', settings.MAX_PAGES)
        page = request.POST.get('page', 1)
        search = request.POST.get('search', None)
    else:
        items_per_page = request.GET.get('items', settings.MAX_PAGES)
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)

    jobs = []

    if org:
        jobs = Job.objects.filter(organization=org)

    if search:
        found = False
        for action_choice in Job.ACTION_CHOICES:
            if search.lower() in action_choice[1].lower():
                jobs = jobs.filter(action=int(action_choice[0]))
                found = True
                break

        if not found:
            jobs = jobs.filter(Q(command__contains=search) |
                               Q(description__contains=search) |
                               Q(path__contains=search) |
                               Q(parameters__contains=search) |
                               Q(pk__contains=search))

    total_pages = math.ceil(decimal.Decimal(len(jobs) / float(settings.MAX_PAGES)))

    jobs = paginate_objects(jobs, items_per_page, page)

    data = serializers.serialize("json", jobs)

    response = HttpResponse(data)

    response['total_pages'] = total_pages

    return response


@csrf_exempt
@require_http_methods(["POST", "GET"])
@login_required(login_url="/login_user/")
def runs(request):
    try:
        org = Account.objects.get(user=request.user).organization
    except Account.DoesNotExist:
        return HttpResponse("[]")

    if request.method == "POST":
        items_per_page = request.POST.get('items', settings.MAX_PAGES)
        page = request.POST.get('page', 1)
        search = request.POST.get('search', None)
    else:
        items_per_page = request.GET.get('items', settings.MAX_PAGES)
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)

    runs = []

    if org:
        runs = Run.objects.filter(organization=org)

    if search:
        runs = Run.filter(Q(command__contains=search) |
                           Q(description__contains=search) |
                           Q(path__contains=search) |
                           Q(parameters__contains=search) |
                           Q(pk__contains=search))

    total_pages = math.ceil(decimal.Decimal(len(runs) / float(settings.MAX_PAGES)))

    runs = paginate_objects(runs, items_per_page, page)

    data = serializers.serialize("json", runs)

    response = HttpResponse(data)

    response['total_pages'] = total_pages

    return response
