"""."""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.InvoiceListView.as_view(), name='invoice-list'),
    url(r'^new/$',
        views.InvoiceNewView.as_view(), name='invoice-new'),
    url(r'^(?P<id>[\w\- ]+)/edit/$',
        views.InvoiceUpdateView.as_view(), name='invoice-edit'),
    url(r'^(?P<id>[^/]+)/delete/$',
        views.InvoiceDeleteView.as_view(), name="invoice-delete"),
]
