# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-21 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concursante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competencia', models.CharField(max_length=150)),
                ('evento', models.CharField(max_length=150)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('aprendices', models.CharField(max_length=1000)),
                ('region', models.CharField(max_length=150)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dia_1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dia_2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dia_3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dia_4', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
    ]
