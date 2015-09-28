# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0011_auto_20141009_2320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drink',
            options={'ordering': ['beerinst__beer__name'], 'get_latest_by': 'date'},
        ),
        migrations.AddField(
            model_name='drink',
            name='datetime',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='drink',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
