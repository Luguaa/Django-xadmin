# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-04-06 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[(b'easy', '\u521d\u7ea7'), (b'normal', '\u4e2d\u7ea7'), (b'hard', '\u9ad8\u7ea7')], max_length=4, verbose_name='\u96be\u5ea6'),
        ),
    ]
