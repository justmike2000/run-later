# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-27 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='timezone',
            field=models.CharField(blank=True, default=b'US/Eastern', max_length=255, null=True),
        ),
    ]
