# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swag', '0002_auto_20180121_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='mob_no',
            field=models.CharField(default=3, max_length=12),
            preserve_default=False,
        ),
    ]
