from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from . models import DebitLog, PaidLog

@receiver(post_save, sender = DebitLog)
@receiver(post_delete, sender = DebitLog)
def calc_total(sender, instance, **kwargs):
    total = instance.customer.debitlog_set.all().filter(paid = False).aggregate(total = Sum('amount')).get('total')
    if total == None:
        total = 0
    instance.customer.total = total - instance.customer.total_paid
    instance.customer.save()

@receiver(post_save, sender = PaidLog)
@receiver(pre_delete, sender = PaidLog)
def calc_total_paid(sender, instance, **kwargs):
    total_paid = instance.customer.paidlog_set.all().aggregate(total = Sum('amount')).get('total')
    if total_paid == None:
        total_paid = 0
    if kwargs.get('created'):
        instance.customer.total_paid = total_paid
        instance.customer.total = instance.customer.total - total_paid
    else:
        instance.customer.total_paid = instance.customer.total_paid - total_paid
        instance.customer.total = instance.customer.total + total_paid
    instance.customer.save()