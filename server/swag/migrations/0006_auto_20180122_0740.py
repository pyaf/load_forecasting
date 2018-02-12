# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('swag', '0005_auto_20180122_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 22, 7, 40, 9, 247260, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='csv',
            name='load_value',
            field=models.FloatField(),
        ),
    ]
