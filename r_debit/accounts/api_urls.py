from knox.views import LogoutView
from django.urls import path

from .api_views import UserApiView, RegisterApiView, LoginApiView

urlpatterns = [
    path('user/', UserApiView.as_view(), name = 'user'),
    path('register/', RegisterApiView.as_view(), name = 'register'),
    path('login/', LoginApiView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout')
]