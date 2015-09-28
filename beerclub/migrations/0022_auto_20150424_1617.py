# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0021_auto_20150424_1612'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='drink',
            index_together=set([('datetime', 'account', 'beerinst'), ('datetime', 'account'), ('date', 'beerinst'), ('datetime', 'beerinst'), ('date', 'account', 'beerinst'), ('date', 'account')]),
        ),
    ]
