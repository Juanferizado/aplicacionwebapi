from django.forms import ModelForm, Textarea
from app.common.models import Services

class ServicesForm(ModelForm):
    class Meta:
        model = Services
        fields = (
        	'name', 
        	'price', 
        	'discount',
            'description', 
       		)
        