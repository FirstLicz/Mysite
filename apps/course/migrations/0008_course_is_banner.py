# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-12 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20180227_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, max_length=1, verbose_name='是否轮播'),
        ),
    ]
