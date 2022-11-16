# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('lead_type', models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('parts', 'Parts'), ('services', 'Services'), ('contact', 'Contact'), ('others', 'Others')], default='others', max_length=10)),
                ('buyer_urgency', models.CharField(choices=[('now', 'Immediate'), ('1to3', '1-3 Months'), ('3to6', '3-6 Months'), ('6to12', '6-12 Months'), ('12to24', '12-24 Months'), ('noidea', 'Dont know yet'), ('others', 'Others')], default='others', help_text='When do you need the Equipment?', max_length=10)),
                ('buyer_manufacturer_details', models.CharField(blank=True, help_text='Manufacturer Details', max_length=500, null=True)),
                ('buyer_model_details', models.CharField(blank=True, help_text='Model Details', max_length=500, null=True)),
                ('buyer_studies_needed', models.TextField(blank=True, help_text='What types of studies do you need a system to perform?', null=True)),
                ('buyer_facility', models.CharField(choices=[('clinic', 'Clinic'), ('hospital', 'Hospital'), ('dia_center', 'Diagnostic Center'), ('others', 'Others')], help_text='Facility', max_length=15)),
                ('buyer_budget', models.CharField(blank=True, max_length=20, null=True)),
                ('seller_type', models.CharField(choices=[('clinic', 'Clinic'), ('hospital', 'Hospital'), ('eqd', 'Equipment Dealer'), ('fin_ins', 'Financial Institution'), ('ser_com', 'Service Company'), ('OEM', 'OEM'), ('part_supp', 'Parts Supplier'), ('others', 'Others')], default='others', max_length=20)),
                ('seller_modality', models.CharField(blank=True, max_length=20, null=True)),
                ('seller_manufacturer_details', models.CharField(blank=True, max_length=500, null=True)),
                ('seller_model_details', models.CharField(blank=True, max_length=500, null=True)),
                ('seller_manufacture_date', models.CharField(blank=True, help_text='Date of Manufacture', max_length=15, null=True)),
                ('seller_reason_for_sale', models.TextField(blank=True, help_text='Describe Your Imaging Project and Reason for Sale', null=True)),
                ('project_timing', models.CharField(choices=[('now', 'Immediate'), ('1to3', '1-3 Months'), ('3to6', '3-6 Months'), ('6to12', '6-12 Months'), ('12to24', '12-24 Months'), ('noidea', 'Dont know yet'), ('others', 'Others')], default='others', help_text='Project Timing', max_length=10)),
                ('is_functional', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('ins', 'Installed'), ('others', 'Others')], default='others', help_text='Functional', max_length=8)),
                ('part_name', models.CharField(blank=True, max_length=100, null=True)),
                ('part_number', models.CharField(blank=True, max_length=100, null=True)),
                ('part_urgency', models.CharField(choices=[('now', 'Immediate'), ('1to3', '1-3 Months'), ('3to6', '3-6 Months'), ('6to12', '6-12 Months'), ('12to24', '12-24 Months'), ('noidea', 'Dont know yet'), ('others', 'Others')], default='others', help_text='When do you need the Part?', max_length=10)),
                ('part_exchange_available', models.CharField(choices=[('y', 'Yes'), ('n', 'No'), ('o', 'Others')], default='O', max_length=2)),
                ('part_description', models.TextField(blank=True, null=True)),
                ('services_pack', models.CharField(choices=[('G', 'GOLD'), ('S', 'SILVER'), ('B', 'BRONZE'), ('O', 'OTHER')], default='O', max_length=2)),
            ],
        ),
    ]