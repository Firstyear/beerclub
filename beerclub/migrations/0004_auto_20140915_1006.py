# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0003_auto_20140912_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='barcode',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beer',
            name='barcode',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
    ]
