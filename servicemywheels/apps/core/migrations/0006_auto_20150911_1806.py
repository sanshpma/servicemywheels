# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150906_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_address_id',
        ),
        migrations.AddField(
            model_name='customeraddresses',
            name='state',
            field=models.CharField(default=b'', max_length=75, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_drop_address_id',
            field=models.ForeignKey(related_name='customer_drop_address_id', blank=True, to='core.CustomerAddresses', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_pickup_address_id',
            field=models.ForeignKey(related_name='customer_pickup_address_id', blank=True, to='core.CustomerAddresses', null=True),
        ),
    ]
