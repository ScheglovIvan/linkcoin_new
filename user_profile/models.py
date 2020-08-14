from django.db.models import *
from django.utils.timezone import now

from register.models import User
from random import choice
from string import ascii_uppercase
from controlled_data.models import Plan

'''
status - pending, failed, completed
type - charge, payout
'''
class PayoutMethod(Model):
    name = CharField(max_length=32, db_index=True, default="")
    user = ForeignKey(User, on_delete=PROTECT)
    recipient_type = CharField(max_length=32, default='')
    recipient = CharField(max_length=100, db_index=True)
    default = BooleanField(default=False) 
    date = DateTimeField(default=now)
    active = BooleanField(default=True) 

    def __str__(self):
        return f'{self.id}) {self.name}'

class Payment(Model):
    amount = FloatField()
    currency = CharField(max_length=3)
    status = CharField(max_length=32)
    user = ForeignKey(User, on_delete=PROTECT)
    plan = ForeignKey(Plan, on_delete=PROTECT, blank=True, null=True, default=None)
    method = CharField(max_length=32)
    date = DateTimeField(default=now)
    share = BooleanField(default=False) 

    def __str__(self):
        return f'{self.id} {self.user.email}'

class Payout(Model):
    amount = FloatField()
    currency = CharField(max_length=10)
    status = CharField(max_length=32)
    user = ForeignKey(User, on_delete=PROTECT)
    method = ForeignKey(PayoutMethod, on_delete=PROTECT)
    date = DateTimeField(default=now)

    @classmethod
    def create(cls, amount, currency, status, user, method):
        payout = cls(amount=amount, currency=currency, status=status, user=user, method=method)
        payout.save()


    def __str__(self):
        return f'{self.id} {self.user.email}'

class Ref_Link(Model):
    ref_link = CharField(max_length=32)
    user = ForeignKey(User, on_delete=PROTECT)
    date = DateTimeField(default=now)
    default = BooleanField(default=False)
    active = BooleanField(default=True)

    @classmethod
    def create(cls, user, ref_link=None):
        all_ref_links = (cls.objects.filter(user=user, active=True))

        if not all_ref_links:
            while True:
                ref_link = ''.join(choice(ascii_uppercase) for i in range(12))
                ref_links = (cls.objects.filter(ref_link=ref_link, active=True))
                if ref_links:
                    pass
                else:
                    break
            ref_link = cls(ref_link=ref_link, user=user, default=True)
            ref_link.save()

            return True
        elif len(all_ref_links) <= 3:
            ref_links = (cls.objects.filter(ref_link=ref_link, active=True))
            
            if not ref_links:
                ref_link = cls(ref_link=ref_link, user=user)
                ref_link.save()

                return True
        
        return False


    @classmethod
    def delete(cls, user, ref_link):
        all_ref_links = (cls.objects.filter(user=user, active=True))
        if len(all_ref_links) > 1:
            ref_links = (cls.objects.filter(user=user, ref_link=ref_link, active=True))
            if ref_links:
                del_ref_link = ref_links[0]
                del_ref_link.active = False
                del_ref_link.save()

                if del_ref_link.default:
                    all_ref_links = (cls.objects.filter(user=user, active=True))
                    if all_ref_links:
                        new_def_ref_link = all_ref_links[0]
                        new_def_ref_link.default = True
                        new_def_ref_link.save()



    def __str__(self):
        return f'{self.ref_link}'

