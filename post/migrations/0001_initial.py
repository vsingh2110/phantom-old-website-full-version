# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('content', tinymce.models.HTMLField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('top_image', models.ImageField(blank=True, upload_to='uploads/posts')),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]