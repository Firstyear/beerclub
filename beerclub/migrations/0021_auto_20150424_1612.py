# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0020_beerinst_stock_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='barcode',
            field=models.CharField(db_index=True, max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beer',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='barcode',
            field=models.CharField(db_index=True, max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beerinst',
            name='barcode_pack',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='brewery',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='drink',
            name='date',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='drink',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='datetime',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='stockwriteoff',
            name='datetime',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
