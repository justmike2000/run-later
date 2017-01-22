# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
        ('servers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('action', models.IntegerField(choices=[(0, 'SSH'), (1, 'HTTP')], default=0)),
                ('command', models.TextField()),
                ('parameters', models.TextField(blank=True, help_text='URL params or STDIN', null=True)),
                ('path', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=512, null=True)),
                ('password', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512)),
                ('action', models.IntegerField(choices=[(0, 'SSH'), (1, 'HTTP')], default=0)),
                ('command', models.TextField()),
                ('parameters', models.TextField(help_text='URL params or STDIN')),
                ('result', models.TextField()),
                ('path', models.CharField(blank=True, max_length=512, null=True)),
                ('username', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('return_code', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cron_string', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.IntegerField(choices=[(0, 'PENDING'), (1, 'RUNNING'), (2, 'COMPLETED')], default=0)),
                ('scheduled', models.DateTimeField(verbose_name='Scheduled time')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servers.Server')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='credentials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.JobCredential'),
        ),
        migrations.AddField(
            model_name='job',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Organization'),
        ),
    ]
