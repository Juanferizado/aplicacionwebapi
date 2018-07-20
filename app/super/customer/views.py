"""Coupons CRUD."""

"""Viws."""
from django.views.generic import TemplateView

from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.common.models import Customer, Invoice
from . import forms
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from app.common.utils import get_deleted_objects
from app.super import mixins
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.template.response import TemplateResponse


class CustomerListView(mixins.SuperPermissionsMixin, ListView):
    """carpeta List View.

    Attributes:
        context_object_name (str): Description
        model (TYPE): Description
        template_name (str): Description
    """

    template_name = 'super/customer/index.html'
    model = Customer
    context_object_name = 'customers'
    paginate_by =  10

    def get_queryset(self):
        """Filter by type and customer.

        Returns:
            TYPE: Description
        """
        queryset = super(CustomerListView, self).get_queryset()
        queryset = Customer.objects.all()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(CustomerListView, self).get_context_data(**kwargs)
        customers = Customer.objects.all()
        context.update({
            'customers': customers,
        })
        return context


class CustomerNewView(CreateView):
    """Prduct Create View."""

    template_name = 'super/customer/new.html'
    model = Customer
    form_class = forms.CustomerForm
    success_url = reverse_lazy('super:customer-list')

    def get_context_data(self, **kwargs):   # noqa
        context = super(CustomerNewView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.save()

        return super(CustomerNewView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Creacion exito"))
        if 'save-and-add' in self.request.POST:
            return reverse('customer-list')
        else:
            return reverse('customer-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class CustomerUpdateView(UpdateView):
    """."""

    template_name = 'super/customer/edit.html'
    model = Customer
    form_class = forms.CustomerForm
    pk_url_kwarg = 'id'
    context_object_name = 'customer'

    def get_queryset(self):
        """Filter by type and customer."""
        queryset = super(CustomerUpdateView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)       
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #self.object = form.save(commit=False)
        #self.object.save()

        return super(CustomerUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Updated success."))
        if 'save-and-add' in self.request.POST:
            return reverse('customer-new')
        else:
            return reverse('customer-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class CustomerDeleteView(DeleteView):
    """."""

    template_name = 'super/customer/delete.html'
    model = Customer
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """Judge Delete."""
        context = super(CustomerDeleteView, self).get_context_data(**kwargs)  # noqa
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
        queryset = super(CustomerDeleteView, self).get_queryset()
        return queryset

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Delete success"))
        return reverse('customer-list')


@require_http_methods(["POST"])
def search(request):
    instance = {}
    queryset = {}
    code_bar = request.POST.get('search')
    invoice =Invoice()
    try:
        queryset = Customer.objects.get(code_bar=code_bar.strip())
        instance = invoice.last_pay(queryset.id)
    except Exception as e:
        return TemplateResponse(request, 'super/customer/customer_status.html', {
            'messages': _('Sin resultados')
            })

    return TemplateResponse(request, 'super/customer/customer_status.html', {
        'messages': _('Cliente encontrado.'),
        'objects': instance, 
        'customer': queryset, 
        'toke_search': code_bar
        })