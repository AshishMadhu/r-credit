from django.core.exceptions import PermissionDenied
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework import permissions as rest_permissions
from rest_framework.authentication import SessionAuthentication

from . import models
from . import serializers
from . import api_permissions

class DebitLogUpdateView(generics.UpdateAPIView):
    queryset = models.DebitLog.objects.all() #! filter by logged in user 
    lookup_url_kwarg = 'debitlog_pk'
    serializer_class = serializers.DebitLogSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [rest_permissions.IsAuthenticated, api_permissions.CheckLogModelsPermission]

class PaidLogViewSet(viewsets.ModelViewSet):
    """
    Created a full Viewset 'cause it is useful in near future
    or you can simply use the UpdateApiView.
    """
    # * better approach
    # inseted of custmer id as url param use debit id
    # get the customer name as data and search for name in debit customer_set if not create new 
    # else create new debit
    model = models.PaidLog
    serializer_class = serializers.PaidLogSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [api_permissions.CheckLogModelsPermission, rest_permissions.IsAuthenticated, ]

    def get_queryset(self):
        customer_pk = self.kwargs.get('customer_pk')
        customer = models.Customer.objects.get(pk = customer_pk)
        return customer.paidlog_set.all()

    def create(self, request, *args, **kwargs):
        try: 
            customer = models.Customer.objects.get(pk = kwargs['customer_pk'])
            if customer.debit.user != request.user:
                raise PermissionDenied
            request.data.update({ 'customer': customer.id })
        except models.Customer.DoesNotExist:
            raise Http404
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        try: 
            customer = models.Customer.objects.get(pk = kwargs['customer_pk'])
            if customer.debit.user != request.user:
                raise PermissionDenied
            request.data.update({ 'customer': customer.id })
        except models.Customer.DoesNotExist:
            raise Http404
        return super().update(request, *args, **kwargs)

class SearchCustomerAPIView(generics.GenericAPIView):
    model = models.Customer
    serializer_class = serializers.CustomerSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [rest_permissions.IsAuthenticated, api_permissions.CheckDebitPermission]

    def get_debit(self, pk):
        try:
            return self.request.user.debit_set.get(pk = pk)
        except models.Debit.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', None)
        debit = self.get_debit(kwargs.get('debit_pk'))
        if name:
            queryset = self.model.objects.filter(name__startswith = name, debit = debit)[:10]
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'You need to pass name as params!'}, status = status.HTTP_400_BAD_REQUEST)