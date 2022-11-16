# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0005_auto_20170907_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(upload_to=b'uploads/resume')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]