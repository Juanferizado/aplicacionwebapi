"""Coupons CRUD."""

"""Viws."""
from django.views.generic import TemplateView

from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.common.models import Invoice
from . import forms
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from app.common.utils import get_deleted_objects
from app.super import mixins

class InvoiceListView(mixins.SuperPermissionsMixin, ListView):
    """carpeta List View.

    Attributes:
        context_object_name (str): Description
        model (TYPE): Description
        template_name (str): Description
    """

    template_name = 'super/invoice/index.html'
    model = Invoice
    context_object_name = 'invoices'
    paginate_by =  10

    def get_queryset(self):
        """Filter by type and customer.

        Returns:
            TYPE: Description
        """
        queryset = super(InvoiceListView, self).get_queryset()
        queryset = Invoice.objects.all()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        invoices = Invoice.objects.all()
        context.update({
            'invoices': invoices,
        })
        return context


class InvoiceNewView(CreateView):
    """Prduct Create View."""

    template_name = 'super/invoice/new.html'
    model = Invoice
    form_class = forms.InvoiceForm
    success_url = reverse_lazy('super:invoice-list')

    def get_context_data(self, **kwargs):   # noqa
        context = super(InvoiceNewView, self).get_context_data(**kwargs)         
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(InvoiceNewView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful creation"))
        if 'save-and-add' in self.request.POST:
            return reverse('invoice-list')
        else:
            return reverse('invoice-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class InvoiceUpdateView(UpdateView):
    """."""

    template_name = 'super/invoice/edit.html'
    model = Invoice
    form_class = forms.InvoiceForm
    pk_url_kwarg = 'id'
    context_object_name = 'Invoice'

    def get_queryset(self):
        """Filter by type and customer."""
        queryset = super(InvoiceUpdateView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs) 
           
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #self.object = form.save(commit=False)
        #self.object.save()

        return super(InvoiceUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Updated success."))
        if 'save-and-add' in self.request.POST:
            return reverse('Invoice-new')
        else:
            return reverse('Invoice-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class InvoiceDeleteView(DeleteView):
    """."""

    template_name = 'super/Invoice/delete.html'
    model = Invoice
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """Judge Delete."""
        context = super(InvoiceDeleteView, self).get_context_data(**kwargs)  # noqa
        #
        deletable_objects, model_count, protected = get_deleted_objects([self.object])  # noqa
        #
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        #
      
        return context

    def get_queryset(self):
        """Filter by type and customer."""
        queryset = super(InvoiceDeleteView, self).get_queryset()
        return queryset

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Delete success"))
        return reverse('invoice-list')