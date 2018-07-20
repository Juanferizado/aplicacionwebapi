from django.forms import ModelForm, Textarea
from app.common.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = (
        	'first_name', 
        	'last_name', 
        	'address',
        	'phone', 
        	'email', 
        	'nit',
            'dpi',
            'code_bar',
       		)
        