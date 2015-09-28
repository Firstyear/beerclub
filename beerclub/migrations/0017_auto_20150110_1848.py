# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0016_auto_20141216_2124'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StockImport',
            new_name='Stock',
        ),
        migrations.RemoveField(
            model_name='stockmove',
            name='beerinst',
        ),
        migrations.DeleteModel(
            name='StockMove',
        ),
    ]
