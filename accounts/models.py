from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey("Organization")

class Organization(models.Model):
    description = models.CharField(max_length=255)
