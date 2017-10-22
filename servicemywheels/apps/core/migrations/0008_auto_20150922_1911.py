# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sendmaillink'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendmaillink',
            name='email_epoch_time',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sendmaillink',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
