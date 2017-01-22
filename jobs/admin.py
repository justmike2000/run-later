from django.contrib import admin

from .models import Job, JobCredential, Run, Schedule


admin.site.register(Job)
admin.site.register(Schedule)
admin.site.register(JobCredential)
admin.site.register(Run)
