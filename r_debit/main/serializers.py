from django.http import request
from django.utils.functional import empty
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class DebitLogSerializer(serializers.ModelSerializer):
    
    customer_name = serializers.ReadOnlyField(source = 'customer.name')
    
    def is_valid(self, raise_exception=False):
        customer_name = self.context['request'].data.pop('customer_name', None)
        if customer_name:
            data = self.context['request'].data
            try:
                customer = models.Customer.objects.filter(debit = self.instance.customer.debit).get(name = customer_name)
                self.instance.customer = customer
            except models.Customer.DoesNotExist:
                raise ValidationError(
                {
                    'customer_name': 'There is no customer with this name!'
                }
            )
        return super().is_valid(raise_exception)

    class Meta: 
        model = models.DebitLog
        exclude = ['id', 'customer', ]


class PaidLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaidLog
        fields = ['id', 'customer', 'amount']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['name', 'id']
