"""."""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.CustomerListView.as_view(), name='customer-list'),
    url(r'^new/$',
        views.CustomerNewView.as_view(), name='customer-new'),
    url(r'^(?P<id>[\w\- ]+)/edit/$',
        views.CustomerUpdateView.as_view(), name='customer-edit'),
    url(r'^search/$',
        views.search, name='customer-search'),
    url(r'^(?P<id>[^/]+)/delete/$',
        views.CustomerDeleteView.as_view(), name="customer-delete"),
]
