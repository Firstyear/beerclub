# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_data_forwards(apps, schema_editor):
    Drink = apps.get_model("beerclub", "Drink")
    for drink in Drink.objects.all():
        try:
            drink.beerinst = drink.beer.beerinst_set.all()[0]
            drink.save()
        except:
            print("Could not add beerinst to replace beer for %s" % drink.beer.name)

class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0008_auto_20141008_0833'),
    ]

    operations = [
        migrations.RunPython(migrate_data_forwards)
    ]
