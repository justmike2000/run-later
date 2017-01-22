from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job, Run

import paramiko
from time import sleep


class Command(BaseCommand):
    help = 'Job Scheduler'

    def add_argument(self, parser):
        pass

    def run_job(self, command):
        return 0, "Output"
        #stdin, stdout, stderr  = self.ssh.exec_command("ls -al")
        #return stdin, stdout, stderr

    def connect(self):
        username = ""
        password = ""

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('localhost', username=username,
                         password=password)

    def handle(self, *args, **kwargs):
        self.connect()

        while 1:
            pass
        while 1:
           jobs = Job.objects.all()

           for job in jobs:
               return_code, output = self.run_job(job.command)

               run = Run.objects.create(description=job.description,
                                        action=job.action,
                                        command=job.command,
                                        parameters=job.parameters,
                                        path=job.path,
                                        return_code=eturn_code,
                                        result=data)
               print run.created_at, ":", job.command

           sleep(1)
