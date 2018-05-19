# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale, Resource, Week


DAYS = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
]



def get_sales():
    data = []
    for x in DAYS:
        data.append(Sale.objects.filter(day=x).aggregate(Avg('value'))['value__avg'])
    return data

def get_sales_month(month="May"):
    data = []
    for x in DAYS:
        data.append(Sale.objects.filter(day=x, month='May').aggregate(Avg('value'))['value__avg'])
    return data

def projection(request, context={}):
    context['month'] = date.today()
    context['sales_avg_historical'] = get_sales()
    context['sales_avg_month'] = get_sales_month()
    context['sales_forecast'] = []

    return render(
        request, 'inputs/projection.html', context
    )


class WeekListView(ListView):

    model = Week

    def get_queryset(self, *args, **kwargs):
        qs = super(WeekListView, self).get_queryset(*args, **kwargs)
        return qs[:20]

    def get_context_data(self, *args, **kwargs):
        data = super(WeekListView, self).get_context_data(*args, **kwargs)
        return data


class WeekDetailView(DetailView):

    model = Week

    def get_context_data(self, *args, **kwargs):
        data = super(WeekDetailView, self).get_context_data(*args, **kwargs)

        if Week.objects.filter(pk=self.get_object().pk+1):
            data['next'] = Week.objects.filter(pk=self.get_object().pk+1)[0]
        else:
            data['next'] = None

        if Week.objects.filter(pk=self.get_object().pk-1):
            data['prev'] = Week.objects.filter(pk=self.get_object().pk-1)[0]
        else:
            data['prev'] = None
        return data
