"""ManejadorDocumentos URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url


from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework.authtoken import views as view_token
from rest_framework_jwt.views import obtain_jwt_token


from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ServicesViewSet)
router.register(r'invoices', views.InviceViewSet)
router.register(r'invoice_detail', views.ServiceInvoiceViewSet)

urlpatterns = [
    url('i18n/', include('django.conf.urls.i18n')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/pay/', views.pay),
    url(r'^api/search/', views.search),

    # url(r'^api-token-auth/', view_token.obtain_auth_token),
    url(r'^app/accounts/', include('allauth.urls')),
    url(r'^', include('app.super.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)