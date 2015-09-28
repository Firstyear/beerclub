# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0004_auto_20140915_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerInst',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('container', models.CharField(help_text=b'Packaging the beer comes in.', max_length=8, choices=[(b'can', b'can'), (b'bottle', b'bottle'), (b'horn', b'horn'), (b'glass', b'glass')])),
                ('volume', models.IntegerField()),
                ('unit_sale_price', models.IntegerField(help_text=b'This is a value in AU cents')),
                ('cost_price', models.IntegerField(help_text=b'This is a value in AU cents')),
                ('special', models.BooleanField(default=False)),
                ('barcode', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('barcode_pack', models.CharField(max_length=50, null=True, blank=True)),
                ('quantity_pack', models.PositiveIntegerField(null=True, blank=True)),
                ('beer', models.ForeignKey(to='beerclub.Beer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
