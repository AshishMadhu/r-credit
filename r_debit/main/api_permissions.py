from rest_framework.permissions import BasePermission

from . import models

class CheckLogModelsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.customer.debit.user == request.user:
            return True
        return False

class CheckDebitPermission(BasePermission):
    def has_permission(self, request, view):
        debit_pk = view.kwargs.get('debit_pk')
        try:
            debit = models.Debit.objects.get(id = debit_pk)
            if request.user == debit.user:
                return True
        except models.Debit.DoesNotExist:
            pass
        return False


