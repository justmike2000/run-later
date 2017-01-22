from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job, Run
from servers.models import Server

import paramiko
from time import sleep


class Command(BaseCommand):
    help = 'Job Scheduler'

    def add_arguments(self, parser):
        parser.add_argument('server_id', nargs='+', type=int)

    def run_job(self, command):
        return 0, "Output"
        #stdin, stdout, stderr  = self.ssh.exec_command("ls -al")
        #return stdin, stdout, stderr

    def connect(self, username, password, host):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('localhost', username=username,
                         password=password)

    def handle(self, *args, **kwargs):
        server_id = kwargs['server_id'][0]

        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            raise Exception("Server Not Defined {}".format(server_id))

        try:
            self.connect(server.credential.username,
                         server.credential.password,
                         server.hostname)
        except paramiko.ssh_exception.BadAuthenticationType:
            raise Exception("Invalid Credentials {}".format(server_id))

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
