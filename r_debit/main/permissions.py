from . import models
class BasePermission:
    def has_permission(self, request, view): 
        return True
    def has_object_permission(self):
        pass

class CheckDebitAccess(BasePermission):
    def has_permission(self, request, view):
        debit = models.Debit.objects.get(pk = view.kwargs.get('debit_pk'))
        if debit.user == request.user:
            return True
        return False

class CheckCustomerAccess(BasePermission):
    def has_permission(self, request, view):
        try:
            customer = models.Customer.objects.get(pk = view.kwargs.get('customer_pk'))
        except models.Customer.DoesNotExist:
            return False
        debit = customer.debit
        if debit.user == request.user:
            return True
        return False

class DeleteDebitLogPermission(BasePermission):
    def has_object_permission(self, request, obj):
        if obj.customer.debit.user == request.user:
            return True
        return False


