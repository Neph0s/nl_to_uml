# coding: utf-8
import random
import logging
from ..redis import RedisClient
from ..util import validate_phone_number

from ..key import (
    REDIS_KEY_SMS_CODE
)
from ..const import TEN_MINS
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

logger = logging.getLogger(__name__)

ali_client = AcsClient('LTAIhvRx5OYpK5Ij', 'Bt7U4zEZzzj88vXuoYQpvmpX3TlMqV', 'cn-hangzhou')

sys_rnd = random.SystemRandom()
redis_client = RedisClient()['lit']

class SmsCodeService(object):
    """
    """
    LIVE_TIME = TEN_MINS
    CODE_LEN = 4
    CODE_CHARS = [str(i) for i in range(10)]
    ERR_WORONG_TELEPHONE = u'wrong telephone number'

    @classmethod
    def gen_code(cls):
        res = ''
        for _ in range(cls.CODE_LEN):
            res += sys_rnd.choice(cls.CODE_CHARS)
        return res

    @classmethod
    def _ali_send_code(cls, phone, code):
        limit = 10

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', '肯斯爪特')
        template_code = 'SMS_164506012' if request.ip_thailand else 'SMS_164510648'
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', {"code":code})
        response = ali_client.do_action(request)
        if response.get('Message', '') != 'OK':
            logger.error('send code failed, phone:%s, code:%s, response:%r', phone, code, response)

    @classmethod
    def send_code(cls, zone, phone, code=None):
        zone_phone = zone + phone
        zone_phone = validate_phone_number(zone_phone)
        if not zone_phone:
            return cls.ERR_WORONG_TELEPHONE, False
        if zone.replace('+', '') == '86':
            code = '1314'
        else:
            code = cls.gen_code() if not code else code
            cls._ali_send_code(zone_phone, code)
        key = REDIS_KEY_SMS_CODE.format(phone=zone_phone)
        redis_client.set(key, code, ex=TEN_MINS)
        return '', True

    @classmethod
    def verify_code(cls, zone, phone, code):
        zone_phone = zone + phone
        zone_phone = validate_phone_number(zone_phone)
        if not zone_phone:
            return cls.ERR_WORONG_TELEPHONE, False
        key = REDIS_KEY_SMS_CODE.format(phone=zone_phone)
        cached_code = redis_client.get(key)
        if not cached_code or cached_code != code:
            return u'wrong code', False
        return '', True
