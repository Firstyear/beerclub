# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0026_auto_20150605_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='barcode',
        ),
    ]
