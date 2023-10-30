from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import MerchandiseMod
from django.views.generic.detail import DetailView


class AllMerchandiseView(TemplateView):
    """
    Gets All Merchandise
    """
    model = MerchandiseMod
    template_name = 'merchandise/all_merch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_merch'] = MerchandiseMod.objects.all()
        return context
