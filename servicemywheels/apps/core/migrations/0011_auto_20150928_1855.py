# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_sendmaillink'),
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
