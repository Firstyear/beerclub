# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerclub', '0017_auto_20150110_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockTake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0)),
                ('beerinst', models.ForeignKey(to='beerclub.BeerInst')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StockWriteOff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=500)),
                ('beerinst', models.ForeignKey(to='beerclub.BeerInst')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='beerinst',
            name='stock_fridge',
        ),
    ]
