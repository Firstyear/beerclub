# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_data_forwards(apps, schema_editor):
    Drink = apps.get_model("beerclub", "Drink")
    for drink in Drink.objects.all():
        drink.payee = drink.account
        drink.save()

class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0024_auto_20150529_1108'),
    ]

    operations = [
        migrations.RunPython(migrate_data_forwards),
    ]
