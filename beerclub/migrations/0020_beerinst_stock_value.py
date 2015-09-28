# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0019_auto_20150401_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='beerinst',
            name='stock_value',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
