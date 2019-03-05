# coding: utf-8
import random

from ..redis import RedisClient
from ..util import validate_phone_number
from ..const import (
    INT_BOY,
    INT_GIRL,
    TWO_WEEKS,
    ONE_DAY,
    USER_NOT_EXISTS
)

from ..key import (
    REDIS_USER_INFO_FINISHED
)
from ..model import (
    User,
    HuanxinAccount
)
from ..service import (
    SmsCodeService,
    FeedService,
    HuanxinService
)

sys_rnd = random.SystemRandom()
redis_client = RedisClient()['lit']

class UserService(object):

    @classmethod
    def login_job(cls, user):
        """
        登录的动作
        :param user:
        :return:
        """
        user.generate_new_session()
        user._set_session_cache(str(user.id))
        if not user.logined:
            user.logined = True
            user.save()

    @classmethod
    def _on_update_info(cls, user):
        cls.update_info_finished_cache(user)

    @classmethod
    def query_user_info_finished(cls, user_id):
        key = REDIS_USER_INFO_FINISHED.format(user_id=str(user_id))
        res =  redis_client.get(key)
        if not res:
            user = User.get_by_id(user_id)
            if not res:
                return False
            return  cls.update_info_finished_cache(user) == 1
        return res == 1

    @classmethod
    def update_info(cls, user_id, data):
        els = ['nickname', 'birthdate', 'avatar', 'bio']
        once = ['gender']
        total_fields = els + once
        field_info = u'field must be at least one of: [%s]' % ','.join(total_fields)
        if not data:
            return field_info, False
        for el in data:
            if el not in total_fields or (not data.get(el) and data.get(el) != False):
                return field_info, False
        has_nickname = 'nickname' in data
        if has_nickname and cls.verify_nickname(data.get('nickname', '')):
            return u'nickname already exists', False
        user = User.get_by_id(user_id)
        if not user:
            return USER_NOT_EXISTS, False
        for el in once:
            if getattr(user, el):
                return u'%s can\'t be reset' % el, False
        for el in data:
            setattr(user, el, data.get(el))
        status = True
        if has_nickname:
            huanxin_id = user.huanxin.user_id
            status = HuanxinService.update_nickname(huanxin_id, data.get('nickname'))
        if status:
            user.save()
            return None, True
        else:
            return u'update huanxin nickname failed', False

    @classmethod
    def update_info_finished_cache(cls, user):
        key = REDIS_USER_INFO_FINISHED.format(user_id=str(user.id))
        res = 1 if user.finished_info else 0
        redis_client.set(key, res, exp=TWO_WEEKS + ONE_DAY)
        return res

    @classmethod
    def create_huanxin(cls):
        huanxin_id = None
        pwd = None
        for i in range(5):
            huanxin_id = HuanxinAccount.gen_id()
            print huanxin_id
            pwd = HuanxinAccount.get_password(huanxin_id)
            status = HuanxinService.create_user(huanxin_id, pwd)
            if status:
                break
        huanxin = HuanxinAccount()
        huanxin.user_id = huanxin_id
        huanxin.password = pwd
        return huanxin

    @classmethod
    def phone_login(cls, zone, phone, code):
        msg, status = SmsCodeService.verify_code(zone, phone, code)
        if not status:
            return msg, status
        zone_phone = validate_phone_number(zone + phone)
        if not zone_phone:
            return cls.ERR_WORONG_TELEPHONE, False
        user = User.get_by_phone(zone_phone)
        if not user:
            user = User()
            user.huanxin = cls.create_huanxin()
            user.phone = zone_phone
            user.save()
            cls.update_info_finished_cache(user)
        cls.login_job(user)

        basic_info = cls.get_basic_info(user)
        login_info = user.get_login_info()
        basic_info.update(login_info)
        return basic_info, True

    @classmethod
    def get_basic_info(cls, user):
        basic_info = user.basic_info()
        basic_info.update({'bio': cls.get_bio(user)})
        return basic_info

    @classmethod
    def get_bio(cls, user):
        if user.bio:
            return user.bio
        feed_num = FeedService.feed_num(str(user.id))
        he_or_she = 'He' if user.gender == INT_BOY else 'She'
        if feed_num > 3:
            return u'%s is mysterious~' % he_or_she
        return u'%s loves to share' % he_or_she

    @classmethod
    def verify_nickname(cls, nickname):   # judge if nickname exists
        if not nickname or User.get_by_nickname(nickname):
            return True
        return False

    @classmethod
    def get_user_info(cls, user_id, target_user_id):
        target_user = User.get_by_id(target_user_id)
        if not target_user:
            return USER_NOT_EXISTS, False
        return cls.get_basic_info(target_user), True

    @classmethod
    def get_avatars(cls):
        return

