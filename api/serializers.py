from django.contrib.auth.models import Group
from app.accounts.models import User
from django.db import transaction
from app.common.models import Services, Customer, Invoice, service_invoice
from rest_framework import serializers
from django.template.defaultfilters import date

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name','last_name','username', 'email')


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class ServicesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Services
		fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):		

	class Meta:
		model = Customer
		fields = (
			'full_name',
			'dpi',)

class InvoiceSerializer(serializers.ModelSerializer):	
	customer_obj = serializers.SerializerMethodField()
	total = serializers.SerializerMethodField()
	year = serializers.SerializerMethodField()
	month = serializers.SerializerMethodField()	

	class Meta:
		model = Invoice 
		fields = '__all__'
		extra_kwargs = {
		   'total': {'max_digits': 16, 'decimal_places': 2}
		}
	
	def get_customer_obj(self, obj):
		"""-"""
		serializers = CustomerSerializer(instance=obj.customer)
		return serializers.data

	def get_total(self, obj):
		"""-"""	    
		return obj.total

	def get_year(self, obj):
		"""-"""	    
		return obj.created_at.year

	def get_month(self, obj):
		"""-"""	    
		return date(obj.created_at, 'F')


class DetailSerializer(serializers.ModelSerializer):		
	service_obj = serializers.SerializerMethodField()
	invoice_obj = serializers.SerializerMethodField()

	class Meta:
		model = service_invoice
		fields = '__all__'

	def get_service_obj(self, obj):
		"""-"""
		serializers = ProductSerializer(instance=obj.service, many=True)
		return serializers.data

	def get_invoice_obj(self, obj):
		"""-"""
		serializers = InvoiceSerializer(instance=obj.invoice, many=True)
		return serializers.data
		
