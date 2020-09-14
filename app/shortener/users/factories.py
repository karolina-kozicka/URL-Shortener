import factory

from . import models

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.User

    email = factory.sequence(lambda n: f"user{n}@example.com")
