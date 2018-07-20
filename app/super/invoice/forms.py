from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory
from djangoformsetjs.utils import formset_media_js

from app.common.models import Invoice

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
        	'customer',        	
        	'description', 
        	'user', 
        	'status',
        	'payment_method',
       		)
