# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.manager
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('customer_name', models.CharField(default=b'', max_length=75, blank=True)),
                ('registered_phone', models.CharField(default=b'', max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                (b'objects', core.manager.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CrewMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('crew_member_name', models.CharField(default=b'', max_length=75, blank=True)),
                ('permanent_address', models.CharField(default=b'', max_length=200, blank=True)),
                ('current_address', models.CharField(default=b'', max_length=200, blank=True)),
                ('email_id', models.EmailField(max_length=75, blank=True)),
                ('zoneid', models.CharField(default=b'', max_length=75, blank=True)),
                ('can_drive', models.CharField(default=b'', max_length=10, blank=True, choices=[(b'Car', b'Car'), (b'Bike', b'Bike'), (b'Both', b'Both')])),
                ('driving_license_number', models.CharField(default=b'', max_length=75, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrewMemberContactNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('crew_member_phone_number', models.CharField(default=b'', max_length=20, blank=True)),
                ('crew_member_id', models.ForeignKey(to='core.CrewMember')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrewMemberIdProof',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('crew_member_id_proof_url', models.FileField(max_length=200, upload_to=b'')),
                ('crew_member_id', models.ForeignKey(to='core.CrewMember')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrewMemberStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'', max_length=50)),
                ('remarks', models.CharField(default=b'', max_length=200)),
                ('crew_member_id', models.ForeignKey(to='core.CrewMember')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerAddresses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('address', models.CharField(default=b'', max_length=200, blank=True)),
                ('zoneid', models.CharField(default=b'', max_length=75, blank=True)),
                ('pincode', models.CharField(default=b'', max_length=10, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('city', models.CharField(default=b'', max_length=75, blank=True)),
                ('country', models.CharField(default=b'', max_length=10, blank=True)),
                ('customer_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerContactNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('phone_number', models.CharField(default=b'', max_length=20, blank=True)),
                ('customer_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerVehicles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('vehicle_number', models.CharField(max_length=20, unique=True, null=True, blank=True)),
                ('vehicle_model', models.CharField(default=b'', max_length=50, blank=True)),
                ('last_serviced_time', models.DateTimeField(null=True, blank=True)),
                ('last_order_number_id', models.IntegerField(null=True, blank=True)),
                ('km_runs', models.CharField(default=b'', max_length=50, blank=True)),
                ('customer_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerVehiclesTypeMake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('vehicle_type', models.CharField(default=b'', max_length=20, choices=[(b'Car', b'Car'), (b'Bike', b'Bike')])),
                ('vehicle_make', models.CharField(default=b'', max_length=50, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('service_center_invoice_url', models.FileField(max_length=200, upload_to=b'')),
                ('our_invoice_url', models.FileField(max_length=200, upload_to=b'')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('order_id', models.CharField(default=b'', max_length=20)),
                ('service_type', models.CharField(default=b'', max_length=4)),
                ('specific_problems_listed', models.CharField(default=b'', max_length=1000, blank=True)),
                ('generic_problems_listed', models.CharField(default=b'', max_length=200, blank=True)),
                ('customer_requested_pickup_time', models.DateTimeField(null=True, blank=True)),
                ('actual_pickup_time', models.DateTimeField(null=True, blank=True)),
                ('sc_delivered_time', models.DateTimeField(null=True, blank=True)),
                ('sc_pickup_time', models.DateTimeField(null=True, blank=True)),
                ('customer_delivered_time', models.DateTimeField(null=True, blank=True)),
                ('zoneid', models.CharField(default=b'', max_length=75, blank=True)),
                ('sc_bill_amount', models.DecimalField(null=True, max_digits=11, decimal_places=4, blank=True)),
                ('handling_charges', models.DecimalField(null=True, max_digits=11, decimal_places=4, blank=True)),
                ('status', models.CharField(default=b'', max_length=75, blank=True)),
                ('sc_chosen_by_customer', models.BooleanField(default=False)),
                ('remarks', models.CharField(default=b'', max_length=200)),
                ('customer_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('customer_vehicle_id', models.ForeignKey(blank=True, to='core.CustomerVehicles', null=True)),
                ('customer_vehicle_type_make', models.ForeignKey(blank=True, to='core.CustomerVehiclesTypeMake', null=True)),
                ('drop_crew_member_id', models.ForeignKey(related_name='drop_crew_member_id', blank=True, to='core.CrewMember', null=True)),
                ('invoice_id', models.ForeignKey(blank=True, to='core.Invoices', null=True)),
                ('pickup_crew_member_id', models.ForeignKey(related_name='pickup_crew_member_id', blank=True, to='core.CrewMember', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('service_center_id', models.CharField(default=b'', unique=True, max_length=20)),
                ('service_center_brand', models.CharField(default=b'', max_length=20)),
                ('service_center_type', models.CharField(default=b'', max_length=10, choices=[(b'Car', b'Car'), (b'Bike', b'Bike')])),
                ('service_center_address', models.CharField(default=b'', max_length=200, blank=True)),
                ('service_center_area_name', models.CharField(default=b'', max_length=50, blank=True)),
                ('service_center_pincode', models.CharField(default=b'', max_length=10, blank=True)),
                ('service_center_zoneid', models.CharField(default=b'', max_length=10, blank=True)),
                ('service_center_emailid', models.EmailField(max_length=75, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCenterContactNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('phone_number', models.CharField(default=b'', max_length=20, blank=True)),
                ('service_center_id', models.ForeignKey(to='core.ServiceCenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCenterContactPersons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('contact_person_name', models.CharField(default=b'', max_length=50, blank=True)),
                ('contact_person_designation', models.CharField(default=b'', max_length=30, blank=True)),
                ('contact_person_emailid', models.EmailField(max_length=75, blank=True)),
                ('contact_person_personal_phone_number', models.CharField(default=b'', max_length=20, blank=True)),
                ('service_center_id', models.ForeignKey(to='core.ServiceCenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='service_center_id',
            field=models.ForeignKey(blank=True, to='core.ServiceCenter', null=True),
        ),
        migrations.AddField(
            model_name='customervehicles',
            name='vehicle_type_make',
            field=models.ForeignKey(blank=True, to='core.CustomerVehiclesTypeMake', null=True),
        ),
        migrations.AddField(
            model_name='crewmemberstatus',
            name='current_order_id',
            field=models.ForeignKey(to='core.Order'),
        ),
    ]
