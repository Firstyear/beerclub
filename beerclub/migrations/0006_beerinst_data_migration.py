# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_data_forwards(apps, schema_editor):
    Beer = apps.get_model("beerclub", "Beer")
    BeerInst = apps.get_model("beerclub", "BeerInst")
    for beer in Beer.objects.all():
        beerinst = BeerInst(beer=beer, container='bottle', volume=beer.volume,
            unit_sale_price=beer.unit_sale_price, cost_price=beer.cost_price,
            special=beer.special, barcode=beer.barcode,
            barcode_pack=beer.barcode_pack, quantity_pack=beer.quantity_pack)
        beerinst.save()

class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0005_beerinst'),
    ]

    operations = [
        migrations.RunPython(migrate_data_forwards)
    ]
