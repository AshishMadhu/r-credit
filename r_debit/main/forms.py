from django import forms
from django.forms import fields, widgets
from django.forms.models import model_to_dict
from . models import Debit, DebitLog, PaidLog

class DebitForm(forms.ModelForm):
    class Meta:
        model = Debit
        fields = ['name', ]
        help_texts = {
            'name': 'RECOMMENTED: If you have a shop then give shop name as debit name'
        }

class DebitLogForm(forms.ModelForm):
    customer_name = forms.CharField(label="Customer Name")

    class Meta:
        model = DebitLog
        fields = ['customer_name', 'amount', 'item_list']
    
class PaidLogForm(forms.ModelForm):
    customer_name = forms.CharField(label = 'Customer Name')

    class Meta:
        model = PaidLog
        fields = ['customer_name', 'amount']