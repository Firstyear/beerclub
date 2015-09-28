# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0012_auto_20141011_0359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drink',
            options={'ordering': ['beerinst__beer__name'], 'get_latest_by': 'datetime'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
