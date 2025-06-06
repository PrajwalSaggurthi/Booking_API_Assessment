from tortoise.models import Model
from tortoise.fields import IntField, CharField, BooleanField, DatetimeField


class Classes(Model):
    id = IntField(pk=True)
    name = CharField(max_length=100, null=False)
    bookings = IntField(null=False)
    date_time = DatetimeField(null=False)
    closed = BooleanField(default=False)


    def __str__(self):
        return self.name

class Bookings(Model):
    id = IntField(pk=True)
    class_id = IntField(null=False)
    user_name = CharField(max_length=100, null=False)
    user_email = CharField(max_length=100, null=False)
    date_time = DatetimeField(null=False)


    def __str__(self):
        return self.user_email