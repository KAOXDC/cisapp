# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-21 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concursante',
            name='dia_1',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='concursante',
            name='dia_2',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='concursante',
            name='dia_3',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='concursante',
            name='dia_4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='concursante',
            name='total',
            field=models.FloatField(),
        ),
    ]
