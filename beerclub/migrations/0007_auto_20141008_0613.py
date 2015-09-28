# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0006_beerinst_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer',
            name='barcode',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='barcode_pack',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='quantity_pack',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='special',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='unit_sale_price',
        ),
        migrations.RemoveField(
            model_name='beer',
            name='volume',
        ),
    ]
