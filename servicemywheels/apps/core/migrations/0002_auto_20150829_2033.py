# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewmemberstatus',
            name='status',
            field=models.CharField(default=b'', max_length=60),
        ),
    ]
