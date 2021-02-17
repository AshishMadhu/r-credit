from accounts.views import SignUpView
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('api-auth/', include(('accounts.api_urls', 'account-api'), namespace = 'api')),
    path('signup', SignUpView.as_view(), name = 'signup'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]