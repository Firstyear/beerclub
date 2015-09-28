# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.IntegerField(help_text=b'This is a value in AU cents. It is reconciled as a set of payments and drinks')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'user__first_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('volume', models.IntegerField()),
                ('abvp', models.FloatField(default=0, null=True, blank=True)),
                ('unit_sale_price', models.IntegerField(help_text=b'This is a value in AU cents')),
                ('cost_price', models.IntegerField(help_text=b'This is a value in AU cents')),
                ('special', models.BooleanField(default=False)),
            ],
            options={
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
            options={
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(to='beerclub.Brewery'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ClubAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('special', models.BooleanField(default=False)),
                ('debt', models.IntegerField(help_text=b'This is a value in AU cents. This value is populated automatically', blank=True)),
                ('date', models.DateField()),
                ('account', models.ForeignKey(to='beerclub.Account')),
                ('beer', models.ForeignKey(to='beerclub.Beer')),
            ],
            options={
                'ordering': [b'beer__name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('caccount', models.ForeignKey(to='beerclub.ClubAccount')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(help_text=b'This is a value in AU cents')),
                ('date', models.DateField()),
                ('account', models.ForeignKey(to='beerclub.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
