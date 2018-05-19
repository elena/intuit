# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView, DetailView

from .models import Sale, Resource, Week


class WeekListView(ListView):

    model = Week

    def get_queryset(self, *args, **kwargs):
        qs = super(WeekListView, self).get_queryset(*args, **kwargs)
        return qs[:10]

    def get_context_data(self, *args, **kwargs):
        data = super(WeekListView, self).get_context_data(*args, **kwargs)
        return data


class WeekDetailView(DetailView):

    model = Week
