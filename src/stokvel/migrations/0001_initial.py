# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-10 18:13
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import stokvel.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Stokvel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rehive_identifier', models.CharField(max_length=2000, unique=True)),
                ('monthly_payment', stokvel.models.MoneyField(decimal_places=18, default=Decimal('0'), max_digits=28)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rehive_identifier', models.CharField(max_length=2000, unique=True)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('stokvel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stokvel.Stokvel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stokvel.User')),
            ],
        ),
        migrations.AddField(
            model_name='stokvel',
            name='users',
            field=models.ManyToManyField(to='stokvel.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='stokvel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stokvel.Stokvel'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ManyToManyField(to='stokvel.User'),
        ),
    ]
