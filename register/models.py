import datetime
import random
import string

from django.db.models import *
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from dateutil.relativedelta import relativedelta
from django.conf import settings

from django.db import transaction
import paypalrestsdk
from django.http import HttpResponse
import requests


class User(AbstractUser):
    balance = FloatField(default=0)
    users_invited = PositiveIntegerField(default=0)
    sub_active_till = DateTimeField(default=datetime.datetime.min, verbose_name='Subscription active till')
    email_code = CharField(max_length=32, null=True, blank=True)
    code_active_till = DateTimeField(default=now)
    last_sent_email = DateTimeField(default=now)
    avatar = ImageField(default='landing/static/landing/images/profile/user.png', upload_to='register/static/register/images/avatars', blank=True, null=True)
    country = CharField(max_length=255, default='', blank=True, null=True)
    region = CharField(max_length=255, default='', blank=True, null=True)
    city = CharField(max_length=255, default='', blank=True, null=True)
    ip = GenericIPAddressField(db_index=True, null=True)
    reward = FloatField(default=20)
    special_user = BooleanField(default=False)

    pp_user_id = CharField(max_length=255, default='', blank=True, null=True)

    def __str__(self):
        return self.email


    def generate_email_code(self, size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def get_avatar_url(self):
        avatar_url = ''

        start = False

        for character in self.avatar.url:
            if not start and (character == '/' or character == '\\'):
                start = True
            elif start:
                avatar_url += character

        return avatar_url

    def get_sub_exp_time(self):
        iso_formatted_date = self.sub_active_till.isoformat()

        splitter = '.' if '.' in iso_formatted_date else '+'

        sub_active_till = datetime.datetime.strptime(iso_formatted_date.split(splitter)[0], '%Y-%m-%dT%H:%M:%S')

        difference = sub_active_till - datetime.datetime.utcnow()

        active = False
        days = hours = minutes = 0

        if difference.total_seconds() > 0:
            active = True
            seconds = difference.seconds
            minutes = seconds // 60
            seconds -= 60 * minutes
            hours = minutes // 60
            minutes -= 60 * hours
            days = difference.days

        return {
            'active': active,
            'minutes': minutes,
            'hours': hours,
            'days': days,
        }

    def renew_subscription(self, months=0, weeks=0, days=0, hours=0, minutes=0):
        active = self.get_sub_exp_time()['active']

        time_delta = relativedelta(months=months, weeks=weeks, days=days, hours=hours, minutes=minutes)

        new_date = self.sub_active_till if active else now()
        new_date += time_delta

        self.sub_active_till = new_date

        self.save()

        return new_date


    @classmethod
    def getReward(cls, id, months_count):
        with transaction.atomic():
            today = now()

            account = (cls.objects.select_for_update().get(id=id))

            if account.sub_active_till > today:
                account.balance += account.reward * months_count
                account.save()

                return True

            return False

    @classmethod
    def payout(cls, id, payout_method, payout_func):
        with transaction.atomic():
            # print("Безопасная функция начало")
            account = (cls.objects.select_for_update().get(id=id))

            balance = account.balance - 1.5
            if payout_func(payout_method, balance) == True:
                account.balance = 0
                account.save()
                # print("Безопасная функция конец")
                return True
            else:
                # print("Безопасная функция конец")
                return HttpResponse(status=403)


    @classmethod
    def PayLinkcoinBalance(cls, id, days, price):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))

            if account.balance < price:
                return False
                
            account.renew_subscription(days=days)

            account.balance = '%.1f' % (account.balance - price)
            account.save()

            return True
    
                    


class Invitation(Model):
    invited = ForeignKey(User, on_delete=PROTECT, related_name='invited')
    inviter = ForeignKey(User, on_delete=PROTECT, related_name='inviter')
    date = DateTimeField(default=now)

    def __str__(self):
        date = str(self.date).split(' ')[0]
        return f'{self.inviter.email} invited {self.invited.email} on {date}'


class PartnerProgram(Model):
    name = CharField(max_length=100, default='', blank=True, null=True)
    user = ForeignKey(User, on_delete=PROTECT, related_name='partner')
    id_name = CharField(max_length=30, default='', blank=True, null=True)
    req_url = CharField(max_length=500, default='', blank=True, null=True)
    status = CharField(max_length=30, default='', blank=True, null=True)
    goal_buy = CharField(max_length=30, default='', blank=True, null=True)
    goal_reg = CharField(max_length=30, default='', blank=True, null=True)


    def sendData(self, clickId, goal, price=None):
        if goal == "register":
            goal = self.goal_reg
        else:
            goal = self.goal_buy

        req_url = self.req_url.format(pp_user_id=clickId, status=self.status, goal=goal, price=price)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(req_url)                    
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        r = requests.get(req_url)

    def __str__(self):
        return f'{self.name}'
