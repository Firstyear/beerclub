# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0009_drink_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drink',
            name='beer',
        ),
    ]
