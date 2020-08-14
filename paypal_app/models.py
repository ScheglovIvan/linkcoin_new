from django.db.models import *
from django.utils.timezone import now
from register.models import User
from controlled_data.models import Plan


# class PayoutMethod(Model):
#     name = CharField(max_length=32, db_index=True, default="")
#     user = ForeignKey(User, on_delete=PROTECT)
#     recipient_type = CharField(max_length=32, default='')
#     recipient = CharField(max_length=100, db_index=True)
#     default = BooleanField(default=False) 
#     date = DateTimeField(default=now)
#     active = BooleanField(default=True) 

#     def __str__(self):
#         return f'{self.id}) {self.name}'
    
# class Plan(Model):
#     name = CharField(max_length=32, default='')
#     plan_id = CharField(max_length=32, db_index=True)
#     price = FloatField(default=0)
#     days = IntegerField(default=0)

#     def __str__(self):
#         return f'{self.id}) {self.name}'

class Order(Model):
    user = ForeignKey(User, on_delete=PROTECT)
    order_id  = CharField(max_length=32, db_index=True, default="")
    plan = ForeignKey(Plan, on_delete=PROTECT)
    date = DateTimeField(default=now)

    def __str__(self):
        return f'{self.id}) {self.user.email}'