# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-19 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputs', '0004_auto_20180519_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='type',
            field=models.CharField(choices=[('timesheet_hours', 'timesheet_hours'), ('payroll_cost', 'payroll_cost')], default='temp', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('date', 'type')]),
        ),
    ]
