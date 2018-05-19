# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Sale(models.Model):

    day = models.CharField(max_length=32)
    date = models.DateField()
    month = models.CharField(max_length=32)
    value = models.FloatField()
    week = models.IntegerField()

    class Meta:
        ordering = ['-week']

    def __str__(self):
            return self.date

class Hour(models.Model):

    date = models.DateField()
    value = models.FloatField()
