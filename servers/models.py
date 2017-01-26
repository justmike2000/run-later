from django.db import models
from django.conf import settings
import os
import signal

class Server(models.Model):
    ACTION_CHOICES = (
        (0, 'SSH'),
        (1, 'HTTP'),
        (2, 'AGENT'),
    )
    hostname = models.CharField(max_length=255, blank=False, null=False)
    credential = models.ForeignKey("Credential")
    pid = models.CharField(max_length=255, blank=True, null=True)
    cert = models.TextField(blank=True, null=True)
    type = models.IntegerField(choices=ACTION_CHOICES, null=False, blank=False)


    def start_server(self):
        self.pid = os.spawnlp(os.P_NOWAIT, "/bin/sh", "{}/spawn_server.sh {}".format(settings.WORKING_DIRECTORY,
                                                                                           self.id))
        self.save()

    def kill_server(self):
        os.kill(self.pid, signal.SIGTERM)

    def __unicode__(self):
        return "{} - {} {} {}".format(self.id,
                                      self.hostname,
                                      self.credential.username, self.pid)


class Credential(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return "{} - {}".format(self.id, self.username)

