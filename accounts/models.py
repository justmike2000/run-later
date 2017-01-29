from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey("Organization")
    timezone = models.CharField(default="US/Eastern", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "{} - {} {}".format(self.id, self.user, self.organization)


class Organization(models.Model):
    description = models.CharField(max_length=255)
    allowed_ips = models.CharField(max_length=255)

    def __unicode__(self):
        return "{} - {}".format(self.id, self.description)