# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0018_auto_20150110_2037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-datetime']},
        ),
        migrations.AlterModelOptions(
            name='stockwriteoff',
            options={'ordering': ['-datetime']},
        ),
    ]
