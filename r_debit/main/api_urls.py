from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main import api_views

router = DefaultRouter()

router.register('paidlog/(?P<customer_pk>[0-9a-f-]+)', api_views.PaidLogViewSet, 'paidlog')

urlpatterns = [
    path('', include(router.urls)),
    path('debitlog/<int:debitlog_pk>/', api_views.DebitLogUpdateView.as_view(), name = 'debitlog-update'),
    path('search-customer/<uuid:debit_pk>/', api_views.SearchCustomerAPIView.as_view(), name = 'search-customer'),
]