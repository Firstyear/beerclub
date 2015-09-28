# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0002_auto_20140912_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='barcode',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beer',
            name='barcode',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beer',
            name='barcode_pack',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beer',
            name='quantity_pack',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='drink',
            name='rating',
            field=models.PositiveIntegerField(default=3, null=True, blank=True),
        ),
    ]
