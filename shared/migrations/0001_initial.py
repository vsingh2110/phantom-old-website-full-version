# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='uploads/shared')),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePageVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('youtube_url', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('show_on_site', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, upload_to='uploads/profile')),
                ('author_name', models.CharField(max_length=50)),
                ('author_title', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
