# coding: utf-8
import datetime
import random
import json
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    IntField,
    ListField,
    StringField,
)
from ..const import (
    ONE_DAY
)
from ..redis import RedisClient

sys_rnd = random.SystemRandom()
redis_client = RedisClient()['lit']


class ExperimentResult(Document):
    meta = {
        'strict': False,
        'alias': 'db_alias'
    }

    exp_name = StringField(required=True)
    tag = StringField()
    result_date = DateTimeField()
    stat_name = StringField()
    res = StringField()
    create_time = DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def create(cls, exp_name, tag, result_date, stat_name, res):
        obj = cls.get_by_args(exp_name, tag, result_date, stat_name)
        if obj:
            return obj
        res = json.dumps(res)
        obj = cls(exp_name=exp_name, tag=tag, result_date=result_date, stat_name=stat_name, res=res)
        obj.save()
        return obj

    @classmethod
    def get_by_args(cls, exp_name, tag, result_date, stat_name):
        return cls.objects(exp_name=exp_name, tag=tag, result_date=result_date, stat_name=stat_name).first()