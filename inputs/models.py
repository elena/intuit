# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Week(models.Model):

    week = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-week']


class Sale(models.Model):

    day = models.CharField(max_length=32)
    date = models.DateField()
    month = models.CharField(max_length=32)
    value = models.FloatField()
    week = models.IntegerField()
    week_fk = models.ForeignKey('inputs.Week', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-week']

    def __str__(self):
        return "{}".format(self.date)


RESOURCE_CHOICES = [
        ('timesheet_hours', 'timesheet_hours'),
        ('payroll_cost', 'payroll_cost')
]

class Resource(models.Model):

    type = models.CharField(max_length=64, choices=RESOURCE_CHOICES)
    week_fk = models.ForeignKey('inputs.Week', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()

    class Meta:
        unique_together = ['date', 'type']