# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swag', '0003_signup_mob_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSV',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
                ('load_value', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='SignUp',
        ),
    ]
