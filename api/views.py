
# Create your views here.

from rest_framework.parsers import  MultiPartParser, FormParser
from rest_framework.decorators import parser_classes, api_view
from django.contrib.auth.models import  Group
from app.accounts.models import User
from rest_framework import authentication
from app.common.models import Services, Invoice, Customer, service_invoice
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ServicesSerializer, InvoiceSerializer, CustomerSerializer, DetailSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from decimal import *
from django.core.mail import send_mail
import nexmo
import os
from django.utils.translation import ugettext_lazy as _


# from rest_framework import serializers 
# from mail_templated import send_mail, EmailMessage
# from django.core.mail import EmailMultiAlternatives
# from django.template import loader, Context
NEXMO_API_KEY = os.environ.get('NEXMO_API_KEY')
NEXMO_API_SECRET = os.environ.get('NEXMO_API_SECRET')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer
    # parser_classes = (FormParser, MultiPartParser,)

    def create(self, request, *args, **kwargs):
        """Summary.

        Args:
            request (TYPE): Description
            *args: Description
            **kwargs: Description

        Returns:
            TYPE: Description
        """                        
        email = self.request.data['email']
        first_name = self.request.data['first_name']
        last_name = self.request.data['last_name']
        password = self.request.data['password']
        password2 = self.request.data['password2']
        exist_user = User.objects.filter(email=email)        
        serializer = UserSerializer(data=request.data)        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ServicesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class InviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        """Summary.

        Args:
            request (TYPE): Description
            *args: Description
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        user = self.request.user
        service_id = self.request.data['service']

        customer_id = self.request.data['customer']        
        discount = self.request.data['discount']        
        description = self.request.data['description']
        try:
            customer = Customer.objects.get(
                pk=customer_id)       

            service = Services.objects.get(
                pk=service_id)        

        except Exception as e:
            return Response('Dato no encontrado', status=status.HTTP_404_NOT_FOUND)
        

        with transaction.atomic():
            invoice = Invoice()
            invoice.correlative = invoice.next_correlative()
            invoice.customer = customer            
            invoice.user = user
            invoice.description = description
            invoice.save()
            # serializer = InvoiceSerializer(invoice)        

            #:::::::save detail invoice                    
            detail = service_invoice()            
            detail.service = service
            detail.price = service.price
            detail.invoice = invoice
            detail.discount = Decimal(discount)            
            detail.save()
                      
        return Response('',status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        """Listado de Detalles de cargos cxc."""
        user = self.request.user  
        customer = Customer.objects.filter(
            user=user)[0]  
        queryset = self.get_queryset()
        queryset = queryset.filter(customer=customer)
        serializer = InvoiceSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceInvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = service_invoice.objects.all()
    serializer_class = DetailSerializer

    def retrieve(self, request, pk=None):
        queryset = product_invoice.objects.all()       
        queryset = queryset.filter(invoice=pk)
        serializer = DetailSerializer(queryset)     
        return Response(serializer.data)



@api_view(['POST'])
def pay(request):
    """Summary.

    Args:
        request (TYPE): Description

    Returns:
        TYPE: Description
    """    
    pay_dates = request.data['pay_dates']

    '''for item in pay_dates:  
        with transaction.atomic():                
            invoice = Invoice.objects.get(id=item["id"], status=True, pay=False)
            if invoice: 
                invoice.pay();
    '''              
    return Response(pay_dates, status=status.HTTP_200_OK)
    # return Response('Llegó la cresta....', status=status.HTTP_201_CREATED)



@api_view(["GET"])
def search(request):    
    instance = {}
    queryset = {}
    serializer_class = InvoiceSerializer
    code_bar = request.GET.get('search')
    try:
        queryset = Customer.objects.get(dpi__contains=code_bar.strip())
        instance = Invoice.objects.filter(customer__id=queryset.id, pay_status=False)        
    except Exception as e:            
        return Response('Dato no encontrado', status=status.HTTP_404_NOT_FOUND)    

    serializer = InvoiceSerializer(instance, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

