from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'

    def get_success_url(self) -> str:
        return reverse('accounts:login')
