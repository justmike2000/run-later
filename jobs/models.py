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

    def __unicode__(self):
        return "{} - {} {} {}".format(self.id, self.description, self.created_at,
                                      self.action)


class JobCredential(models.Model):
    username = models.CharField(max_length=512, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField('Date created', auto_now_add=True, blank=False)

    def __unicode__(self):
        return "{} - {}".format(self.id, self.username)


class Run(models.Model):
    description = models.CharField(max_length=512, blank=False)
    action = models.IntegerField(choices=Job.ACTION_CHOICES, blank=False,
                                 null=False, default=0)
    command = models.TextField(null=False, blank=False)
    parameters = models.TextField(null=False, blank=False, help_text="URL params or STDIN")
    result = models.TextField(null=False, blank=False)
    path = models.CharField(max_length=512, blank=True, null=True)
    username = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField('Date created', auto_now_add=True, blank=False)
    def __unicode__(self):
        return "{} {} {} {}".format(self.description, self.action, self.command, self.created_at)
