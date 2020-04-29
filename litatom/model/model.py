# coding: utf-8
import datetime
import random
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    IntField,
    ListField,
    StringField,
)
from .. key import (
    REDIS_ADMIN_USER
)
from ..const import (
    ONE_DAY
)
from ..model import (
    User
)
from ..redis import RedisClient

sys_rnd = random.SystemRandom()
redis_client = RedisClient()['lit']


class Model(Document):
    meta = {
        'strict': False,
        'alias': 'db_alias'
    }

    user_id = StringField(required=True, unique=True)
    create_time = DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def get_by_user_name(cls, user_name):
        return cls.objects(user_name=user_name).first()