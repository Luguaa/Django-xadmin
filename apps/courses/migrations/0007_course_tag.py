# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-04-12 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default=b'', max_length=10, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]
