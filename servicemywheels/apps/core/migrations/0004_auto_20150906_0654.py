# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_address_id',
            field=models.ForeignKey(blank=True, to='core.CustomerAddresses', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
