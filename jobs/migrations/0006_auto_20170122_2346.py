# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-22 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_schedule_scheduled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='scheduled',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Scheduled time'),
        ),
    ]
