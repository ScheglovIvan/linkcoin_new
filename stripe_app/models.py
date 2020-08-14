from django.db.models import *

class Plan(Model):
    name = CharField(max_length=32, default='')
    plan_id = CharField(max_length=32, db_index=True)

    def __str__(self):
        return f'{self.id}) {self.name}'
