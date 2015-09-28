# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0010_remove_drink_beer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beerinst',
            options={'ordering': ['beer__name']},
        ),
    ]
