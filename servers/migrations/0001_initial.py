# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('pid', models.CharField(blank=True, max_length=255, null=True)),
                ('cert', models.TextField(blank=True, null=True)),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servers.Credential')),
            ],
        ),
    ]
