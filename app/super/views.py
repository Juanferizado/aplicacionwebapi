"""Viws."""
from django.views.generic import TemplateView

from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from . import mixins

class HomeSuperView(mixins.SuperPermissionsMixin, TemplateView):
    """HomeView.

    Attributes:
        template_name (str): Description
        user_types (TYPE): Description
    """

    template_name = 'super/index.html'

    def get_context_data(self, **kwargs):   # noqa
        """Summary

        Args:
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        context = super(HomeSuperView, self).get_context_data(**kwargs)
       
        return context

