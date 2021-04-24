from django.urls import path, include

from .views import (CreateDebit, CustomerListView, DebitDeleteView, DebitListView, DebitLogCreateView, DebitLogDeleteView,
                    DebitLogListView, PaidLogCreateView, PaidLogListView)

app_name = 'main'

urlpatterns = [
    path('', DebitListView.as_view(), name = 'debit-list'),
    path('api/', include(('main.api_urls', 'main-api'), namespace = 'api')),
    path('debit-delete/<debit_pk>/', DebitDeleteView.as_view(), name = 'debit-delete'),
    path('debit-create/', CreateDebit.as_view(), name = 'create-debit'),
    path('debitlog-create/<uuid:debit_pk>/', DebitLogCreateView.as_view(), name = 'debitlog-create'),
    path('debitlog/<uuid:customer_pk>/', DebitLogListView.as_view(), name = 'debitlog-list'),
    path('debitlog-delete/<int:debitlog_pk>', DebitLogDeleteView.as_view(), name = 'debitlog-delete'),
    path('customerlog/<uuid:debit_pk>/', CustomerListView.as_view(), name = 'customer-log'),
    path('paidlog-create/<uuid:debit_pk>/', PaidLogCreateView.as_view(), name = 'paidlog-create'),
    path('paidlog/<uuid:customer_pk>/', PaidLogListView.as_view(), name = 'paidlog-list'),
]
