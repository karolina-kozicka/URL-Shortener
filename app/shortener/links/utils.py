from django.utils.crypto import get_random_string

from . import models


def create_hash():
    while True:
        hash = get_random_string(10)
        try:
            models.Link.object.get(hash=hash)
        except:
            break
    return hash

