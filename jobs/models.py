from __future__ import unicode_literals

from django.db import models


class Job(models.Model):
    ACTION_CHOICES = (
        (0, 'SSH'),
        (1, 'HTTP'),
    )
    description = models.CharField(max_length=512, blank=False)
    created_at = models.DateTimeField('Date created', auto_now_add=True, blank=False)
    action = models.IntegerField(choices=ACTION_CHOICES, blank=False, null=False, default=0)
    command = models.TextField(null=False, blank=False)
    parameters = models.TextField(null=True, blank=True, help_text="URL params or STDIN")
    path = models.CharField(max_length=512, blank=True, null=True)
    credentials = models.ForeignKey("JobCredential", null=True, blank=True)
    organization = models.ForeignKey("accounts.Organization")

    def __unicode__(self):
        return "{} - {} {} {}".format(self.id, self.description, self.created_at,
                                      self.action)


class JobCredential(models.Model):
    username = models.CharField(max_length=512, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField('Date created', auto_now_add=True, blank=False)

    def __unicode__(self):
        return "{} - {}".format(self.id, self.username)



class Schedule(models.Model):
    STATUS_CHOICES = (
        (0, 'PENDING'),
        (1, 'RUNNING'),
        (2, 'COMPLETED'),
    )
    job = models.ForeignKey("Job")
    server = models.ForeignKey("servers.Server", blank=True, null=True)
    cron_string = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    scheduled = models.DateTimeField('Scheduled time', auto_now_add=False, blank=False)

    def __unicode__(self):
        return "{} - {} {} {} {} {}".format(self.id, self.job.command, self.scheduled,
                                            self.status, self.server, self.cron_string)


class Run(models.Model):
    description = models.CharField(max_length=512, blank=False)
    action = models.IntegerField(choices=Job.ACTION_CHOICES, blank=False,
                                 null=False, default=0)
    command = models.TextField(null=False, blank=False)
    parameters = models.TextField(null=False, blank=False,
                                  help_text="URL params or STDIN")
    result = models.TextField(null=False, blank=False)
    path = models.CharField(max_length=512, blank=True, null=True)
    username = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField('Date created', auto_now_add=True, blank=False)
    return_code = models.IntegerField(default=-1)

    def __unicode__(self):
        return "{} {} {} {}".format(self.description, self.action, self.command, self.created_at)
