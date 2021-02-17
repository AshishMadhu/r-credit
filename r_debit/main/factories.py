import factory
import factory.fuzzy
from django.contrib.auth.models import User

from main import models

class UserFactory(factory.django.DjangoModelFactory):
  username = factory.Faker('user_name')
  # username = factory.Sequence(lambda n: "user_%d" % n)
  password = factory.PostGenerationMethodCall('set_password', 'TestPass@123')
  first_name = factory.Faker('first_name')
  last_name = factory.Faker('last_name')
  email = factory.LazyAttribute(lambda a: '{}.{}@hiestAsh.com'.format(a.first_name, a.last_name))

  class Meta:
    model = User
    django_get_or_create = ('username', )

class DebitFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.sequence(lambda n: "shop_%d" % n)

    class Meta:
        model = models.Debit

class CustomerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('user_name')
    debit = factory.SubFactory(DebitFactory)

    class Meta:
        model = models.Customer

class DebitLogFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    amount = factory.fuzzy.FuzzyDecimal(10, 1000, 0)

    class Meta:
        model = models.DebitLog
    
class PaidLogFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    amount = factory.fuzzy.FuzzyDecimal(10, 1000, 0)

    class Meta:
        model = models.PaidLog
