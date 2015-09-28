# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='barcode',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='barcode_pack',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='quantity_pack',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='drink',
            name='rating',
            field=models.PositiveIntegerField(default=3, null=True),
            preserve_default=True,
        ),
    ]
