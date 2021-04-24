import logging
from typing import Any, Dict

from django import http
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView

from . import forms, mixins, models, permissions

logger = logging.getLogger(__name__)

class CreateDebit(LoginRequiredMixin, CreateView):
    model = models.Debit
    fields = ['name', ]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        instance = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Debit {} created, Now you can add your debit list here :)'.format(instance.name))
        url = instance.get_absolute_url()
        return HttpResponseRedirect(url)

class DebitListView(LoginRequiredMixin, ListView):
    model = models.Debit
    paginate_by = 10
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'debit_form': forms.DebitForm,
        })
        return ctx

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(user = self.request.user).order_by('name')

class DebitDeleteView(LoginRequiredMixin, mixins.PermissionCheckMixin, DeleteView):
    permission_classes = [permissions.CheckDebitObjAccess, ]
    model = models.Debit
    pk_url_kwarg = 'debit_pk'

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        # just need a response 'success' to refresh the page
        return HttpResponse('success')

class DebitLogCreateView(LoginRequiredMixin, mixins.PermissionCheckMixin, CreateView):
    model = models.DebitLog
    form_class = forms.DebitLogForm
    permission_classes = [permissions.CheckDebitAccess, ]

    def get_initial(self) -> Dict[str, Any]:
        # To autofill customer name on form
        if self.request.GET.get("customer_name"):
            return {
                'customer_name': self.request.GET.get("customer_name")
            }
        super().get_initial()

    def get_customer(self, form: BaseModelForm):
        return models.Customer.objects.get_or_create(
            name=form['customer_name'].value().title(),
            debit_id=self.kwargs.get('debit_pk')
        )
        
    def get_customer(self, form: BaseModelForm):
        try:
            logger.info('Creating DebitLog with already created customer')
            return [models.Customer.objects.get(
                name=form['customer_name'].value(),
                debit_id=self.kwargs.get('debit_pk')
            ), False]
        except models.Customer.DoesNotExist:
            try:
                return models.Customer.objects.get_or_create(
                    name=form['customer_name'].value().title(),
                    debit_id=self.kwargs.get('debit_pk')
                )
            except:
                pass
        return None

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        customer, created = self.get_customer(form) # not created update debit log
        debit = customer.debit
        form.instance.customer = customer
        instance = form.save()
        return HttpResponseRedirect(instance.get_absolute_url())

class DebitLogListView(LoginRequiredMixin, mixins.PermissionCheckMixin, ListView):
    paginate_by = 6
    permission_classes = [permissions.CheckCustomerAccess, ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # to show customer name
        ctx = super().get_context_data(**kwargs)
        customer = models.Customer.objects.get(pk = self.kwargs.get('customer_pk'))
        ctx.update({
            'customer': customer,
            'debit_id': customer.debit.id,
            'debitlog_form': forms.DebitLogForm,
        })
        return ctx

    def get_queryset(self) -> QuerySet:
        sort_arg = self.request.GET.get('sort') or '-date'
        paid_arg = self.request.GET.get('paid', False)
        customer = models.Customer.objects.get(pk = self.kwargs.get('customer_pk'))
        return customer.debitlog_set.all().filter(paid = paid_arg).order_by(sort_arg)

class DebitLogDeleteView(LoginRequiredMixin, mixins.PermissionCheckMixin, DeleteView):
    # todo Bettter create an api view *It was a long day for me*
    permission_classes = [permissions.DeleteDebitLogPermission, ]
    model = models.DebitLog
    pk_url_kwarg = 'debitlog_pk'

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        # just need a response 'success' to refresh the page
        return HttpResponse('success')

class CustomerListView(LoginRequiredMixin, mixins.PermissionCheckMixin, ListView):
    paginate_by = 6
    allow_empty = True
    permission_classes = [permissions.CheckDebitAccess, ]
    template_name = 'main/customer_list.html'

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            models.Debit.objects.get(pk=self.kwargs.get('debit_pk'))
        except:
            raise Http404('Page not found')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # debit_id is need to create a link for debit log create view in template
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'debit_id': self.kwargs.get('debit_pk'),
            'debitlog_form': forms.DebitLogForm,
        })
        return ctx

    def get_queryset(self) -> QuerySet:
        # todo should come with a better approach
        # sort_arge with non-field param will rise exception
        sort_arg = self.request.GET.get('sort') or '-date'
        name = self.request.GET.get('name') or None

        sort_args_list = ['customer__name', '-customer__name', 'customer__total', '-customer__total', 'date', '-date']
        if not sort_arg in sort_args_list:
            messages.add_message(self.request, messages.ERROR, 'Invalid sort parameter!')
            logger.error('Invalid sort')
            sort_arg = '-date'
        debit = models.Debit.objects.get(pk=self.kwargs.get('debit_pk'))
        customers = debit.customer_set.all()
        queryset = models.DebitLog.objects.all().filter(amount = None).values(
            'customer__name',
            'customer__total',
            'customer__total_paid',
            'customer__pk',
            ).annotate(date = Max('date'))
        for customer in customers:
            qs = customer.debitlog_set.all().filter().values(
                'customer__name',
                'customer__total',
                'customer__total_paid',
                'customer__pk',
                ).annotate(date = Max('date'))
            queryset = queryset | qs
        if name:
            qs_by_name = queryset.filter(customer__name = name)
            if len(qs_by_name):
                queryset = qs_by_name
            else:
                messages.add_message(self.request, messages.ERROR, 'Customer name not found!')
        return queryset.order_by(sort_arg)

class PaidLogCreateView(LoginRequiredMixin, mixins.PermissionCheckMixin, CreateView):    
    template_name = 'main/paidlog_form.html'
    form_class = forms.PaidLogForm
    permission_classes = [permissions.CheckDebitAccess, ]

    def get_initial(self) -> Dict[str, Any]:
        # To autofill customer name on form
        if self.request.GET.get("customer_name"):
            return {
                'customer_name': self.request.GET.get("customer_name")
            }
        super().get_initial()

    def get_customer(self, form: BaseModelForm):
        # first check with name normally if not exist then check its titled version
        # eg, shibu -not found then, titled version Shibu 
        try:
            return models.Customer.objects.get(
                name=form['customer_name'].value(),
                debit_id=self.kwargs.get('debit_pk')
            )
        except models.Customer.DoesNotExist:
            try:
                return models.Customer.objects.get(
                    name=form['customer_name'].value().title(),
                    debit_id=self.kwargs.get('debit_pk')
                )
            except:
                pass
        return None

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        debit = models.Debit.objects.get(pk = self.kwargs.get('debit_pk'))
        customer = self.get_customer(form)
        if customer:
            form.instance.customer = customer
            form.save()
            messages.add_message(self.request, messages.SUCCESS, '{} paid {}. Added successfully'.format(customer.name, form['amount'].value()))
        else:
            messages.add_message(self.request, messages.ERROR, 'Customer name not found!')
            return HttpResponseRedirect(reverse('main:customer-log', kwargs = {'debit_pk': debit.pk}))
        return HttpResponseRedirect(reverse('main:paidlog-list', kwargs = {'customer_pk': customer.pk}))

class PaidLogListView(LoginRequiredMixin, mixins.PermissionCheckMixin, ListView):
    paginate_by = 10
    permission_classes = [permissions.CheckCustomerAccess, ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        customer = models.Customer.objects.get(pk = self.kwargs.get('customer_pk'))
        ctx.update({
            'customer': customer,
            'debit_id': customer.debit.id,
            'paidlog_form': forms.PaidLogForm,
        })
        return ctx

    def get_queryset(self) -> QuerySet:
        sort_arg = self.request.GET.get('sort') or '-datentime'
        customer = models.Customer.objects.get(pk = self.kwargs.get('customer_pk'))
        return models.PaidLog.objects.filter(customer = customer).order_by(sort_arg)