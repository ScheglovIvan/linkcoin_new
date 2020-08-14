from django.db.models import *
from django.core.validators import MinValueValidator

class Leader(Model):
    username = CharField(max_length=64)

    total_click = PositiveIntegerField(default=0)
    total_signup = PositiveIntegerField(default=0)
    total_purchase = PositiveIntegerField(default=0)

    last_month_click = PositiveIntegerField(default=0)
    last_month_signup = PositiveIntegerField(default=0)
    last_month_purchase = PositiveIntegerField(default=0)

    monthly_free = PositiveIntegerField(default=0)
    bonus = PositiveIntegerField(default=0)

    avatar = ImageField(default='landing/static/landing/images/profile/user.png', upload_to='linkcoin/static/controlled_data/images/avatars', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        avatar_url = ''

        start = False

        for character in self.avatar.url:
            if not start and (character == '/' or character == '\\'):
                start = True
            elif start:
                avatar_url += character

        return avatar_url

class PayoutControl(Model):
    amount = FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.amount)

class Rank(Model):
    add = PositiveIntegerField()

    def __str__(self):
        return f'{self.id}'

class Plan(Model):
    name = CharField(max_length=32, default='')
    old_price = FloatField(default=0)
    price = FloatField(default=0)
    days = IntegerField(default=0)

    def __str__(self):
        return f'{self.id}) {self.name}'
