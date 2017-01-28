from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.conf import settings
from django.db.models import Q

from runlater.utils import paginate_objects
from accounts.models import Account
from jobs.models import Job


@csrf_exempt
@require_http_methods(["POST", "GET"])
@login_required(login_url="/login/")
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
        jobs = jobs.filter(Q(command__contains=search) |
                           Q(description__contains=search) |
                           Q(path__contains=search) |
                           Q(parameters__contains=search) |
                           Q(action__contains=search) |
                           Q(pk__contains=search))

    total_pages = (len(jobs) / settings.MAX_PAGES)

    jobs = paginate_objects(jobs, items_per_page, page)

    data = serializers.serialize("json", jobs)

    response = HttpResponse(data)

    response['total_pages'] = total_pages

    return response
