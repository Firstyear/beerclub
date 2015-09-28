# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0022_auto_20150424_1617'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='drink',
            index_together=set([]),
        ),
    ]
