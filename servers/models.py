from django.db import models


class Server(models.Model):
    hostname = models.CharField(max_length=255, blank=False, null=False)
    credential = models.ForeignKey("Credential")
    pid = models.CharField(max_length=255)

class Credential(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)

