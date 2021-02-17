from typing import Any, Optional
from django import http
from django.db import models
from django.http import request
from django.http.response import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

class PermissionCheckMixin(object):
    permission_classes = []

    def permission_denied(self):
        raise PermissionDenied()

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]
    
    def check_permission(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied()
    
    def check_object_permission(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, obj):
                self.permission_denied()

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.check_permission(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset = None) -> models.Model:
        obj = super().get_object(queryset=queryset)
        self.check_object_permission(self.request, obj)
        return obj
    