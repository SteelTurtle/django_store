# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 04:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
