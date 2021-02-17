from uuid import uuid4

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Debit(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)

    def get_absolute_url(self):
        return reverse('main:customer-log', kwargs={'debit_pk': self.id})

    def __str__(self) -> str:
        return '{} debit:- {}'.format(self.name, self.user) 

class DebitLog(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    item_list = models.TextField(max_length=140, blank = True)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('main:debitlog-list', kwargs = {'customer_pk': self.customer.pk})

    def get_item_list(self):
        return self.item_list.split('\n')

    def get_local_time(self):
        return self.date.astimezone(pytz.timezone('Asia/Calcutta'))

    def __str__(self) -> str:
        return '{} - log:- {}'.format(self.customer.name, self.amount)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=140)
    debit = models.ForeignKey(Debit, on_delete=models.CASCADE)
    total = models.IntegerField(default=0, editable=False)
    total_paid = models.PositiveIntegerField(default=0, editable=False)

    def get_last_update_date(self):
        return self.debitlog_set.all().last().date

    def __str__(self) -> str:
        return '{}'.format(self.name)

class PaidLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    datentime = models.DateTimeField(auto_now=True) # date and time
    amount = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {}'.format(self.customer.name, self.amount)
