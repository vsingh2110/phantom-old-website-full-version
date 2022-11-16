# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_brochure'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=50)),
                ('text', tinymce.models.HTMLField(blank=True, null=True)),
                ('help_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]