# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-14 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stokvel', '0004_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='stokvel',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
