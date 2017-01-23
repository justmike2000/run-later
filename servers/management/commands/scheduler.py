from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job, Run, Schedule
from servers.models import Server

import paramiko
from time import sleep
import select


class Command(BaseCommand):
    help = 'Job Scheduler'

    def add_arguments(self, parser):
        parser.add_argument('server_id', nargs='+', type=int)

    def run_job(self, schedule):
        command = schedule.job.command
        #channel = self.client.get_transport().open_session()
        stdin, stdout, stderr = self.client.exec_command(command)
        self.channels.append([schedule, stdout])


    def connect(self, username, password, host):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(host,
                                username=username,
                                password=password)
        except paramiko.ssh_exception.BadAuthenticationType:
            raise Exception("Invalid Credentials {}".format(server_id))

    def log_job(self, job, return_code, output=None):
        log = Run.objects.create(description=job.description,
                                 action=job.action,
                                 command=job.command,
                                 parameters=job.parameters,
                                 path=job.path,
                                 return_code=return_code,
                                 result=output)
        return log

    def complete_job(self, schedule, return_code, output):
        schedule.status = 2
        schedule.save()
        log = self.log_job(schedule.job, return_code, output)
        print schedule.job, "Done!"

    def complete_jobs(self):
        done_jobs = []

        for instance in self.channels:
            schedule, stdout = instance

            return_code = stdout.channel.exit_status_ready()
            if return_code:
                output = stdout.read()
                self.complete_job(schedule, return_code, output)
                done_jobs.append(instance)

        for done_job in done_jobs:
            self.channels.remove(done_job)


    def get_schedules(self, server):
        schedules = Schedule.objects.filter(server=server, status=0)
        for schedule in schedules:
            schedule.status = 1
            schedule.save()
        return schedules

    def handle(self, *args, **kwargs):

        self.channels = []

        server_id = kwargs['server_id'][0]

        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            raise Exception("Server Not Defined {}".format(server_id))

        self.connect(server.credential.username,
                     server.credential.password,
                     server.hostname)

        while 1:
            schedules = self.get_schedules(server)
            for schedule in schedules:
                self.run_job(schedule)

            self.complete_jobs()

            sleep(1)

