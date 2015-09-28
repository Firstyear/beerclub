# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0007_auto_20141008_0613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drink',
            options={'ordering': ['beerinst__beer__name']},
        ),
        migrations.AddField(
            model_name='drink',
            name='beerinst',
            field=models.ForeignKey(default=1, to='beerclub.BeerInst'),
            preserve_default=False,
        ),
    ]
