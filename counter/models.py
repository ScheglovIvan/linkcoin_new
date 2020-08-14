import datetime

from django.db.models import *
from django.utils.timezone import now
from register.models import User
from user_profile.models import Ref_Link

class Visit(Model):
    # ref_link = CharField(max_length=255, default=None, null=True, blank=True, db_index=True)
    ref_link = ForeignKey(Ref_Link, on_delete=PROTECT, default=None, blank=True, null=True)
    user = ForeignKey(User, on_delete=PROTECT, default=None, blank=True, null=True)
    ip = GenericIPAddressField(db_index=True)
    device_type = CharField(max_length=6, db_index=True)
    country = CharField(max_length=255)
    region = CharField(max_length=255)
    city = CharField(max_length=255)
    date = DateTimeField(default=now)

    def __str__(self):
        return f'{self.ip}'
        # return f'{self.ip} {f", ?ref={self.ref_link}" if self.ref_link else str()}'
