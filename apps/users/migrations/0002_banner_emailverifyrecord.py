# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('img', models.ImageField(upload_to=b'banner/%Y/%m', verbose_name='\u8f6e\u64ad\u56fe')),
                ('url', models.URLField(verbose_name='\u8bbf\u95ee\u5730\u5740')),
                ('index', models.IntegerField(default=100, verbose_name='\u987a\u5e8f')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u8f6e\u64ad\u56fe',
                'verbose_name_plural': '\u8f6e\u64ad\u56fe',
            },
        ),
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20, verbose_name='\u9a8c\u8bc1\u7801')),
                ('email', models.EmailField(max_length=50, verbose_name='\u90ae\u7bb1')),
                ('send_type', models.CharField(max_length=10, choices=[(b'register', '\u6ce8\u518c'), (b'get', '\u627e\u56de\u5bc6\u7801')])),
                ('send_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '\u90ae\u7bb1\u9a8c\u8bc1\u7801',
                'verbose_name_plural': '\u90ae\u7bb1\u9a8c\u8bc1\u7801',
            },
        ),
    ]
