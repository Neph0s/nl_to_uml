# coding: utf-8
import datetime
import json
import bson
import cPickle
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    IntField,
    ListField,
    StringField,
    FloatField
)
from ..redis import RedisClient
from ..const import (
    USER_ACTIVE
)
from ..util import (
    cached_property
)
from ..key import (
    REDIS_USER_MODEL_CACHE
)
redis_client = RedisClient()['lit']


class UserModel(Document):
    meta = {
        'strict': False,
        'alias': 'db_alias'
    }
    ALERT_TIMES = 3
    user_id = StringField(required=True)
    alert_num = IntField(required=True, default=0)
    match_times = IntField(default=0)
    total_match_inter = FloatField(default=0)
    create_time = DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def create(cls, user_id):
        # if cls.get_by_user_id(user_id):
        #     return True
        obj = cls(user_id=user_id)
        obj.save()
        return obj

    @cached_property
    def avr_match(self):
        if self.match_times == 0:
            return -1
        return self.total_match_inter / self.match_times

    @classmethod
    def get_by_user_id(cls, user_id):
        cache_key = REDIS_USER_MODEL_CACHE.format(user_id=user_id)
        cache_obj = redis_client.get(cache_key)
        if cache_obj:
            return cPickle.loads(cache_obj)
        obj = cls.objects(user_id=user_id).first()
        redis_client.set(cache_key, cPickle.dumps(obj), USER_ACTIVE)
        return obj

    @classmethod
    def _disable_cache(cls, user_id):
        redis_client.delete(REDIS_USER_MODEL_CACHE.format(user_id=user_id))

    def save(self, *args, **kwargs):
        if getattr(self, 'user_id', ''):
            self._disable_cache(str(self.user_id))
        super(UserModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if getattr(self, 'user_id', ''):
            self._disable_cache(str(self.user_id))
        super(UserModel, self).delete(*args, **kwargs)

    @classmethod
    def add_alert_num(cls, user_id):
        ''' add alert num, return should block now'''
        obj = cls.get_by_user_id(user_id)
        if not obj:
            obj = cls(user_id=user_id, alert_num=1)
        else:
            obj.alert_num += 1
        obj.save()
        if obj.alert_num != 0 and obj.alert_num % cls.ALERT_TIMES == 0:
            return True
        return False

    @classmethod
    def add_match_record(cls, user_id, inter_time_total, times_total=1):
        obj = cls.ensure_model(user_id)
        obj.total_match_inter += inter_time_total
        obj.match_times += times_total
        obj.save()
        return True

    @classmethod
    def ensure_model(cls, user_id):
        obj = cls.get_by_user_id(user_id)
        if not obj:
            obj = cls.create(user_id)
        return obj


class Uuids(Document):
    meta = {
        'strict': False,
        'alias': 'db_alias'
    }
    uuid = StringField(required=True)
    create_time = DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def create(cls, uuid):
        obj = cls.objects(uuid=uuid).first()
        if not obj:
            obj = cls(uuid=uuid)
            obj.save()
        return str(obj.id)