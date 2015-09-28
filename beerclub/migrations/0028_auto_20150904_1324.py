# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0027_remove_account_barcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beerinst',
            name='cost_price',
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='barcode',
            field=models.CharField(null=True, default=None, max_length=50, blank=True, unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='barcode_pack',
            field=models.CharField(default=None, max_length=50, null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='quantity_pack',
            field=models.PositiveIntegerField(default=6, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='unit_sale_price',
            field=models.IntegerField(default=400, help_text=b'This is a value in AU cents'),
        ),
    ]
