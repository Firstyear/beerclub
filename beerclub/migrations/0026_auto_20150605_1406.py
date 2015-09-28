# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0025_fix_drink_payee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['user__first_name'], 'permissions': (('can_login', 'Can login'),)},
        ),
        migrations.AlterField(
            model_name='drink',
            name='payee',
            field=models.ForeignKey(related_name='drink_payee_set', to='beerclub.Account'),
        ),
    ]
