import datetime
import factory
from django.utils import timezone
 

from . import models
from shortener.users.factories import UserFactory

class LinkFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = models.Link

    url = factory.Sequence(lambda n: f"original-url{n}")
    hash = factory.Sequence(lambda n: f"hash{n}")
    user = factory.SubFactory(UserFactory)
    valid_date = timezone.now() + datetime.timedelta(days=15)
    views = 0
        