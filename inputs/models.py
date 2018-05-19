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


class Resource(models.Model):

    week_fk = models.ForeignKey('inputs.Week', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()
