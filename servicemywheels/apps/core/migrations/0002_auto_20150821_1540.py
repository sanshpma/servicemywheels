# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customers',
            managers=[
                ('objects', core.manager.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='customers',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
