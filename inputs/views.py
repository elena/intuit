# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale, Resource, Week


def projection(request, context={}):
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
