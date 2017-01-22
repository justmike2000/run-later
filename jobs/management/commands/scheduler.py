from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job, Run

import paramiko
from time import sleep


class Command(BaseCommand):
    help = 'Job Scheduler'

    def add_argument(self, parser):
        pass

    def run_job(self, command):
        stdin, stdout, stderr  = self.ssh.exec_command("ls -al")
        return stdin, stdout, stderr

    def handle(self, *args, **kwargs):
       username = ""
       password = ""

       self.ssh = paramiko.SSHClient()
       self.ssh.set_missing_host_key_policy(
                 paramiko.AutoAddPolicy())
       self.ssh.connect('localhost', username=username,
                         password=password)
       while 1:
           jobs = Job.objects.all()

           for job in jobs:
               stdin, stdout, stderr = self.run_job(job.command)
               data = stdout.read()

               run = Run.objects.create(description=job.description,
                                        action=job.action,
                                        command=job.command,
                                        parameters=job.parameters,
                                        path=job.path,
                                        result=data)
               print run.created_at, ":", job.command

           sleep(1)
