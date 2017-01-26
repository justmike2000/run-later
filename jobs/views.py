from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core import serializers

from accounts.models import Account
from jobs.models import Job


@require_http_methods(["POST", "GET"])
@login_required(login_url="/login/")
def jobs(request):
    org = Account.objects.get(user=request.user).organization

    jobs = []

    if org:
        jobs = Job.objects.filter(organization=org)

    data = serializers.serialize("json", jobs)

    return HttpResponse(data)
