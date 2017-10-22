# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150906_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='from_login',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='social_id',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='token_etag',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
