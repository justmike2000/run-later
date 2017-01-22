from django.contrib import admin

from .models import Job, JobCredential, Run


admin.site.register(Job)
admin.site.register(JobCredential)
admin.site.register(Run)
