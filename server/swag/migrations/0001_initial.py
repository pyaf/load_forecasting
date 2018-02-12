# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(max_length=120, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updaated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
