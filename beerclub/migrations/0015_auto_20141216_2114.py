# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0014_auto_20141215_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('beerinst', models.ForeignKey(to='beerclub.BeerInst')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StockMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('beerinst', models.ForeignKey(to='beerclub.BeerInst')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='beerinst',
            name='stock_fridge',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beerinst',
            name='stock_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
