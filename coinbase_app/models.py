from django.db.models import *
from django.utils.timezone import now
from register.models import User
from controlled_data.models import Plan


class CoinbaseOrder(Model):
    user = ForeignKey(User, on_delete=PROTECT)
    order_id = CharField(max_length=200, db_index=True, default="")
    plan = ForeignKey(Plan, on_delete=PROTECT)
    date = DateTimeField(default=now)
    paid = BooleanField(default=False) 

    def __str__(self):
        return f'{self.id}) {self.user.email}'
