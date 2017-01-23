from django.db import models
from django.conf import settings
import subprocess


class Server(models.Model):
    hostname = models.CharField(max_length=255, blank=False, null=False)
    credential = models.ForeignKey("Credential")
    pid = models.CharField(max_length=255, blank=True, null=True)
    cert = models.TextField(blank=True, null=True)

    def start_server(self):
        proc = subprocess.Popen(["/bin/sh", "-c", "./spawn_server.sh {}".format(self.id)],
                                cwd=settings.WORKING_DIRECTORY)
        try:
            outs, errs = proc.communicate(timeout=15)
            self = proc.pid
            self.save()
        except:
            proc.kill()
            outs, errs = proc.communicate()

    def __unicode__(self):
        return "{} - {} {} {}".format(self.id,
                                      self.hostname,
                                      self.credential.username, self.pid)


class Credential(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return "{} - {}".format(self.id, self.username)

