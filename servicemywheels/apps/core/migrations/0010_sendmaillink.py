# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150928_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMailLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_deleted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('email_epoch_time', models.IntegerField(null=True, blank=True)),
                ('customer_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
