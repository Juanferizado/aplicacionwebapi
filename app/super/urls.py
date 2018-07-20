from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.HomeSuperView.as_view(), name="home_super"),
    url(r'^products/', include('app.super.products.urls')),
    url(r'^customers/', include('app.super.customer.urls')),
    url(r'^invoices/', include('app.super.invoice.urls')),


]
