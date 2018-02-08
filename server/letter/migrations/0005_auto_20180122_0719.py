# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0004_auto_20180122_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csv',
            name='timestamp',
            field=models.TimeField(),
        ),
    ]
