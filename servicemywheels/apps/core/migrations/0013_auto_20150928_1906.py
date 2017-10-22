# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_sendmaillink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmaillink',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='sendmaillink',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='sendmaillink',
            name='modified_at',
        ),
    ]
