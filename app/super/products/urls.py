"""."""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.ProductListView.as_view(), name='product-list'),
    url(r'^new/$',
        views.ProductNewView.as_view(), name='product-new'),
    url(r'^(?P<id>[\w\- ]+)/edit/$',
        views.ProductUpdateView.as_view(), name='product-edit'),
    url(r'^(?P<id>[^/]+)/delete/$',
        views.ProductDeleteView.as_view(), name="product-delete"),
    url(r'^search/(?P<token>[\w])', views.search, name="search"),
]
