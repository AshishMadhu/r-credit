from django.contrib import admin
from . models import Debit, DebitLog, Customer, PaidLog

admin.site.register(Debit)
admin.site.register(DebitLog)
admin.site.register(Customer)
admin.site.register(PaidLog)
