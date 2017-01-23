from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job, Run, Schedule
from servers.models import Server

import paramiko
from time import sleep


class Command(BaseCommand):
    help = 'Job Scheduler'

    def add_arguments(self, parser):
        parser.add_argument('server_id', nargs='+', type=int)

    def run_job(self, schedule):
        client = self.connect(schedule.server.credential.username,
                              schedule.server.credential.password,
                              schedule.server.hostname)
        command = schedule.job.command

        chan = client.get_transport().open_session()
        chan.exec_command(command)
        return_code = chan.recv_exit_status()
        print command, return_code

    def connect(self, username, password, host):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host,
                           username=username,
                           password=password)
            return client
        except paramiko.ssh_exception.BadAuthenticationType:
            raise Exception("Invalid Credentials {}".format(server_id))

    def log_job(self, job):
        log = Run.objects.create(description=job.description,
                                 action=job.action,
                                 command=job.command,
                                 parameters=job.parameters,
                                 path=job.path,
                                 return_code=0,
                                 result=data)
        return log

    def handle(self, *args, **kwargs):
        server_id = kwargs['server_id'][0]

        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            raise Exception("Server Not Defined {}".format(server_id))

        while 1:
            schedules = Schedule.objects.filter(server=server)

            for schedule in schedules:
                self.run_job(schedule)

                #log = self.log_job(schedule.job)
                #print log.created_at, ":", schedule.job.command

            sleep(1)
