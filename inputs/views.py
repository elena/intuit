# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db.models import Avg, Sum
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

MONTH = "May"

GOAL_SALES = 1.05
GOAL_STAFF = 0.95
TARGET_STAFF = .25

THIS_FY = date(2017,7,1)

def projection(request, context={}):
    context['month'] = date.today()
    sales_avg_historical = Sale.objects.all().aggregate(Avg('value'))['value__avg']*7
    sales_avg_month = Sale.objects.filter(month='May').aggregate(Avg('value'))['value__avg']*7
    sales_forecast = ((sales_avg_month+sales_avg_historical)/2)*GOAL_SALES
    context['sales_avg_historical'] = [sales_avg_historical]
    context['sales_avg_month'] = [sales_avg_month]
    context['sales_forecast'] = [sales_forecast]


    staff_avg_historical = Resource.objects.all().aggregate(Avg('value'))['value__avg']
    staff_avg_month = Resource.objects.filter(date__month=5).aggregate(Avg('value'))['value__avg']

    staff_forecast = staff_avg_historical*GOAL_STAFF
    staff_target = sales_forecast*TARGET_STAFF

    context['staff_avg_historical'] = [staff_avg_historical]
    context['staff_avg_month'] = [staff_avg_month]
    context['staff_forecast'] = [staff_forecast]
    context['staff_target'] = [staff_target]

    [x['value__sum'] for x  in Sale.objects.filter(date__gt=THIS_FY).values('week').annotate(Sum('value'))]
    graph_sales_weekly = Sale.objects.filter(date__gt=THIS_FY).values('week').annotate(Sum('value'))
    context['graph_labels'] = Week.objects.filter(start_date__gt=THIS_FY).order_by('start_date')
    context['graph_sales_weekly'] = graph_sales_weekly
    context['graph_staff_weekly'] = Resource.objects.filter(date__gt=THIS_FY).order_by('date')

    return render(
        request, 'inputs/projection.html', context
    )


def get_sales_by_day():
    data = []
    for x in DAYS:
        data.append(Sale.objects.filter(day=x).aggregate(Avg('value'))['value__avg'])
    return data

def get_sales_by_day_month(month="May"):
    data = []
    for x in DAYS:
        data.append(Sale.objects.filter(day=x, month='May').aggregate(Avg('value'))['value__avg'])
    return data

def projection_day(request, context={}):
    context['month'] = date.today()
    context['sales_avg_historical'] = get_sales_by_day()
    context['sales_avg_month'] = get_sales_by_day_month()
    context['sales_forecast'] = []

    return render(
        request, 'inputs/projection_day.html', context
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

        number = self.get_object().sale_set.aggregate(Sum('value'))['value__sum']*.25
        actual = Resource.objects.filter(week_fk=self.get_object()).first()
        data['number'] = number
        data['actual'] = actual.value
        data['good'] = number < actual.value
        print(number > actual.value)


        if Week.objects.filter(pk=self.get_object().pk+1):
            data['next'] = Week.objects.filter(pk=self.get_object().pk+1)[0]
        else:
            data['next'] = None

        if Week.objects.filter(pk=self.get_object().pk-1):
            data['prev'] = Week.objects.filter(pk=self.get_object().pk-1)[0]
        else:
            data['prev'] = None
        return data
