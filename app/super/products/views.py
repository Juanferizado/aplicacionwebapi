"""Coupons CRUD."""

"""Viws."""
from django.views.generic import TemplateView

from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.common.models import Services
from . import forms
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from app.common.utils import get_deleted_objects
from app.super import mixins
from django.views.decorators.http import require_http_methods
from django.core import serializers
from api.serializers import ServicesSerializer


class ProductListView(mixins.SuperPermissionsMixin, ListView):
    """carpeta List View.

    Attributes:
        context_object_name (str): Description
        model (TYPE): Description
        template_name (str): Description
    """

    template_name = 'super/products/index.html'
    model = Services
    context_object_name = 'servies'
    paginate_by =  10

    def get_queryset(self):
        """Filter by type and customer.

        Returns:
            TYPE: Description
        """
        queryset = super(ProductListView, self).get_queryset()
        queryset = Services.objects.all()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context


class ProductNewView(CreateView):
    """Prduct Create View."""

    template_name = 'super/products/new.html'
    model = Services
    form_class = forms.ServicesForm
    success_url = reverse_lazy('super:product-list')

    def get_context_data(self, **kwargs):   # noqa
        context = super(ProductNewView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        image=[]
        if 'ids_image[]' in self.request.POST:
            image = self.request.POST.getlist('ids_image[]')
            self.object.picture.set(image)

        return super(ProductNewView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Creacion exito"))
        if 'save-and-add' in self.request.POST:
            return reverse('product-list')
        else:
            return reverse('product-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(UpdateView):
    """."""

    template_name = 'super/products/edit.html'
    model = Services
    form_class = forms.ServicesForm
    pk_url_kwarg = 'id'
    context_object_name = 'producto'

    def get_queryset(self):
        """Filter by type and customer."""
        queryset = super(ProductUpdateView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):   # noqa
        context = super(ProductUpdateView, self).get_context_data(**kwargs)       
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        image=[]
        if 'ids_image[]' in self.request.POST:
            image = self.request.POST.getlist('ids_image[]')
            self.object.picture.set(image)

        return super(ProductUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Updated success."))
        if 'save-and-add' in self.request.POST:
            return reverse('product-new')
        else:
            return reverse('product-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(DeleteView):
    """."""

    template_name = 'super/products/delete.html'
    model = Services
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """Judge Delete."""
        context = super(ProductDeleteView, self).get_context_data(**kwargs)  # noqa
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
        queryset = super(ProductDeleteView, self).get_queryset()
        return queryset

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Delete success"))
        return reverse('product-list')


@require_http_methods(["GET"])
def search(request, token):
    instance = {}   
    
    queryset = Product.objects.filter(name__startswith=token)  
    if queryset.count() > 0:                
        serialized_obj = ProductSerializer(queryset, many=True)
        from django.http import JsonResponse
        return JsonResponse(serialized_obj.data, safe=False)
    else:        
        return HttpResponse('No hay coincidencias.', status=503)      
    
