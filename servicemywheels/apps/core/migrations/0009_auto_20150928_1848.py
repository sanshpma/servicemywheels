# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150922_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmaillink',
            name='customer_id',
        ),
        migrations.DeleteModel(
            name='SendMailLink',
        ),
    ]
