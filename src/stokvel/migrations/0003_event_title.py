# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-10 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stokvel', '0002_event_payout'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]