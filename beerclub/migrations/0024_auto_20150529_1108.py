# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0023_auto_20150424_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='payee',
            field=models.ForeignKey(related_name='drink_payee', default=1, to='beerclub.Account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='drink',
            name='special',
            field=models.BooleanField(default=None),
        ),
    ]
