# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('priority', models.IntegerField(default=10)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
