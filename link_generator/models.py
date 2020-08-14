import string
from random import choice
from string import ascii_uppercase

from django.db.models import *

class Link(Model):
    value = CharField(max_length=255, editable=False, null=True, db_index=True)

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        id = self.id

        letters = string.ascii_letters

        total_letters = len(letters)

        value = ''

        while True:
            value = ''.join(choice(ascii_uppercase) for i in range(12))
            if Link.objects.filter(value=value):
                pass
            else:
                break

        self.value = value

        super().save(*args, **kwargs)
