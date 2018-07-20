# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
import uuid
from colorfield.fields import ColorField
from django.db.models import Sum
from decimal import *
from django.db import transaction
from datetime import datetime, timedelta
from app.accounts.models import User
from django.utils.crypto import get_random_string

# Create your models here.
ANULADO_BOOL = 0
ACTIVA = 1  # ABIERTA, ACTIVA, ACTIVA
CERRADO = 'C'

EN_TRANSITO = 'T'
DELIVERED = 'E'
ANULADO = '9'
ESTATUS_CHOISE_SHIPPING = (
    (EN_TRANSITO, _('In transit')),
    (DELIVERED, _('Delivered')),
    (ANULADO, _('Canceled')),
)

CREDIT = 'R'
CASH = 'C'

CHOISE_TYPE_MOVEMENT = (
    (CREDIT, _('Credit')),
    (CASH, _('Cash')),
)

CHECK = 'H'
CHASH = 'C'
DEPOSIT = 'D'
TRANSFER = 'T'
CREDIT_CARD = 'R'
DEBIT_CARD = 'E'

CHOISE_PAYMENT_METHOD = (
    (CHECK, _('Check')),
    (CHASH, _('Cash')),
    (DEPOSIT, _('Deposit')),
    (TRANSFER, _('Transfer')),
    (CREDIT_CARD, _('Credit Card')),
    (DEBIT_CARD, _('Debit Card')),
)

ONLINE = 'O'
STORE = 'S'

CHOISE_SHOP_PLACE = (
    (ONLINE, _('Online')),
    (STORE, _('Store')),
)


class Customer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField( null=False,max_length=255,
        blank=False, verbose_name=_('Last name'))
    last_name = models.CharField(max_length=255,
       null=False, blank=False, verbose_name=_('Firts name'))
    address = models.CharField(max_length=400,
       null=False, blank=False, verbose_name=_('Address'))
    phone = models.CharField(max_length=20,
        null=False, blank=False, verbose_name=_('Phone')) 
    email = models.EmailField(
        null=False, blank=False, verbose_name=_('Email')) 
    nit = models.CharField( max_length=20,
        null=False, blank=False, verbose_name=_('NIT'))
    dpi = models.CharField( max_length=20,
        null=False, blank=False, verbose_name=_('DPI'))
    code_bar = models.CharField( max_length=50,
        null=True, blank=True, verbose_name=_('Code bar'))
    created_at = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        default_related_name = 'customer'
        db_table = 'customer'
        ordering = ['-created_at']

    def __unicode__(self):
        u"""Customer."""
        # return u'%s' % self.full_name
        return str(self.name)

    def __str__(self):
            return self.full_name 

    @property
    def full_name(self):
        """Nombre completo del cliente.

        :attribute: full_name
        :type: String
        :return: self.get_full_name()
        """
        return self.get_full_name()        

    def get_full_name(self):
        u"""Devuelve el nombre completo del cliente.

        Devuelve una unión de el nombre y el apellido del cliente.

        :return: u'%s %s' % (self.first_name, self.last_name)
        """
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """."""       
        # invoice = self.__class__.objects.all() 
        self.code_bar = get_random_string(length=32)
        super(self.__class__, self).save(*args, **kwargs)
    

class Services(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=75, null=False,
        blank=False, verbose_name=_('Name'))
    status = models.BooleanField(
       null=False, blank=False, default=True,  verbose_name=_('Status'))
    price = models.DecimalField(
        null=False, blank=False, max_digits=18, decimal_places=10, verbose_name=_('Price')) 
    description = models.CharField(  max_length=400,
         null=True, blank=True, verbose_name=_('Description'))
    discount = models.DecimalField( max_digits=18,  decimal_places=10, 
         null=True, blank=True, verbose_name=_('Discount'))
    created_at = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        default_related_name = 'service'
        db_table = 'product'
        ordering = ['-created_at']

    def __unicode__(self):
        u"""Product."""
        return self.name

    def __str__(self):
            return u'%s (%s)' % (self.name, self.code )
      

class Invoice(models.Model):

    """docstring for Invoice"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    correlative = models.IntegerField(_('correlative'), null=False, blank=False)
    status = models.BooleanField(default=True, verbose_name=_('Status'))    
    customer = models.ForeignKey( Customer, 
        null=False, 
        blank=False,  
        verbose_name=_('Customer'),  
        related_name=_('customers'),
        on_delete=models.PROTECT)
    user = models.ForeignKey( User, 
        null=False, 
        blank=False,  
        verbose_name=_('User'),  
        related_name=_('Users'),
        on_delete=models.PROTECT)
    payment_method = models.CharField(
        null=False, 
        blank=False,
        default=CHASH,
        max_length=1,
        choices=CHOISE_PAYMENT_METHOD, 
        verbose_name=_('Payment method'))
    description = models.TextField( 
        null=True, blank=True, verbose_name=_('Description'))
    document_number = models.TextField( 
        null=True, blank=True, verbose_name=_('Document number'))
    pay_date = models.DateField(null=True, blank=True, verbose_name=_('Pay date'))
    pay_status = models.BooleanField(default=False, verbose_name=_('Pay'))
    created_at = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        db_table = 'invoice'
        ordering = ['-created_at']

    def __unicode__(self):
        u"""Invoice."""
        return self.correlative 

    def __str__(self):
            return str(self.correlative )

    @property
    def total(self):
        """Total de pedidos.

        Returns:
            Decimal: Devuelve el valor total de todos los gastos de un pedido
        """
        total = 0.00
        filter_total = self.invoices.filter(invoice__status=True, status=True )

        if filter_total.count() > 0:    
            total = float(self.invoices.values_list('subtotal').aggregate(Sum('subtotal'))['subtotal__sum'])            

        if total:
            return round(total,2)
        return round(total,2)

    def anular(self):
        u"""Anular transacción ."""
        if self.status != 0:            
            with transaction.atomic():
                self.invoices.update(status=ANULADO_BOOL)
                self.status = ANULADO_BOOL
                self.save()

    def last_pay(self, customer_id, month=False):
        u"""Ultimo pago realizado al servicio."""
        result = Invoice.objects.filter(customer__id=customer_id, status=True, pay=False)            
        
        #if result.count() > 0:            
        #    if not month:
                # months_num = (datetime.now().date() - result[0].pay_date).days
        #         return months_num
        #    if month:
        #        return result[0].pay_date
        return result

    def clean(self):
        """."""
        super(self.__class__, self).clean()

    def next_correlative(self):
        """Total de pedidos.

        Returns:
            Decimal: Devuelve el valor total de todos los gastos de un pedido
        """
        total = self.invoices.count()

        if total > 0:
            return total + 1
        return 1

    def pay(self):
        u"""Ultimo pago realizado al servicio."""
        self.pay = True
        self.save()                

    def save(self, *args, **kwargs):
        """."""
        # invoice = self.__class__.objects.all()
        invoice = Invoice.objects.all()
        self.correlative = invoice.count()        
        super(self.__class__, self).save(*args, **kwargs)


class service_invoice(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey( Services,
        blank=False, 
        null=False, 
        verbose_name=_('Services'), 
        related_name='products_invoice',
        on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice, 
        null=False, 
        blank=False,  
        verbose_name=_('Invoice'), 
        related_name='invoices',
        on_delete=models.PROTECT)
    status = models.BooleanField(
        default=True,  verbose_name=_('Status'))
    price = models.DecimalField(
        null=False, 
        blank=False, 
        max_digits=18, 
        decimal_places=10, 
        verbose_name=_('Price')) 
    subtotal = models.DecimalField(  
        null=True, 
        blank=True, 
        max_digits=18, 
        decimal_places=10, 
        verbose_name=_('Sub total'))
    discount = models.DecimalField(
        null=False, 
        blank=False, 
        max_digits=18, 
        decimal_places=2, 
        verbose_name=_('discount'))
    description = models.TextField( 
        null=True, 
        blank=True, 
        max_length=255, 
        verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now=True)


    class Meta:  # noqa
        verbose_name = _('Detail invoice')
        verbose_name_plural = _('Details invoice')
        default_related_name = 'productsinvoice'
        db_table = 'product_invoice'

    def __unicode__(self):
        u"""Retorna la descripción de la lista de precio."""
        return self.descripcion

    def anular(self):
        u"""Anular transacción ."""
        if self.status != ANULADO:            
            self.status = ANULADO
            self.save()

    def save(self, *args, **kwargs):
        """."""       
        # invoice = self.__class__.objects.all() 
        self.subtotal = self.price
        super(self.__class__, self).save(*args, **kwargs)

            



