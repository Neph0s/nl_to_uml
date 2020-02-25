# coding: utf-8
import urllib
import base64
import hashlib
import json
import time
import logging
import requests as rq
rq.adapters.DEFAULT_RETRIES = 5  # 增加重连次数

import traceback
from urllib2 import urlopen

import oss2

from ..const import (
    ONE_HOUR,
    PLATFORM_ANDROID,
    PLATFORM_IOS
)

logger = logging.getLogger(__name__)
import requests as req
from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...

class GoogleService(object):
    '''
    https://developers.google.com/identity/sign-in/android/backend-auth
    '''
    CLIENT_ID = '272687572250-i5659eubkl38ck9n17mrijl0neh7rgkc.apps.googleusercontent.com'
    CLIENT_SECRET = 'ZHDIw49zszjoNpVmzV3n6OYD'
    CODE = '4/wwHY-EekKYF1DrHN3Pu_GrsxShOZdko5ipTe-e-yqT2RBWJyc-rs7dCHiNHDTXo6HyJiXWlA5XAj13ZyTmdfxXA'
    IOS_CLIENT_ID = '787479292864-bgpar2s95tbkmjphofq23ivu0b2tdu9t.apps.googleusercontent.com'
    @classmethod
    def login_info(cls, token, platform=PLATFORM_ANDROID):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            client_id = cls.IOS_CLIENT_ID if platform == PLATFORM_IOS else cls.CLIENT_ID
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

            '''idinfo = {u'picture': u'https://lh6.googleusercontent.com/-k2KzgpaOHxg/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rcIYSdTEK8c7XzOKFZU07cQDA2z6Q/s96-c/photo.jpg',
            u'aud': u'272687572250-i5659eubkl38ck9n17mrijl0neh7rgkc.apps.googleusercontent.com', u'family_name': u'wang', u'iss': u'https://accounts.google.com',
            u'email_verified': True, u'name': u'yapeng wang', u'locale': u'zh-CN', u'given_name': u'yapeng', u'exp': 1553580984,
            u'azp': u'272687572250-q38h6dlnru40d39fa0cbais936r93064.apps.googleusercontent.com', u'iat': 1553577384, u'email': u'wangyapeng822@gmail.com',
             u'sub': u'104859548364407961110'}'''
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # userid = idinfo['sub']
            return idinfo
        except ValueError, e:
            # Invalid token
            # print e
            logger.error('log false token:%s, %s', token, e)
            return None


    @classmethod
    def get_accesstoken(cls, code=None):
        url = 'https://accounts.google.com/o/oauth2/token'
        redirect_uri = 'http://www.litatom.com/hello'
        datas = {
            "grant_type": "authorization_code",
            "code": "4/wwHGVxUL6wmwx75MC1bvRr1i_S0jQuj3ldhKxbO-CL1mzyPgECZS332EK9KfrEXzeO1kKIullQZC3K95Lpk4xhY" if not code else code,
            "client_id": cls.CLIENT_ID,
            "client_secret": cls.CLIENT_SECRET,
            "redirect_uri": redirect_uri
        }
        params = urllib.urlencode(datas)
        real_url = url + "?%s" % params
        response = req.post(real_url, verify=False).json()
        # response = requests.post(cls.SEND_URL, verify=False, headers=headers, json=data).json()
        print response



class FacebookService(object):
    '''
    https://blog.csdn.net/mycwq/article/details/71308186
    '''
    #APP_ID = '372877603536187'
    #APP_SECRET = '29e68240c95ceddbe0a6798400ce2f0a'
    APP_ID = '2249012795165840'
    APP_SECRET = '5d59b1c43df07c9ef2441abf19d6bfe9'
    APP_TOKEN = '%s|%s' % (APP_ID, APP_SECRET)

    @classmethod
    def _get_user_id(cls, token):
        try:
            url = 'https://graph.facebook.com/debug_token?access_token=%s&input_token=%s' % (cls.APP_TOKEN, token)
            s = rq.session()
            s.keep_alive = False  # 关闭多余连接
            response = s.get(url, verify=False).json()
            # print response
            assert response.get('data')['is_valid']
            return response.get('data', {}).get('user_id', None)
        except Exception, e:
            logger.error(traceback.format_exc())
            # traceback.print_exc()
            logger.error('Error get , token: %r, err: %r', token, e)
            return None

    @classmethod
    def _get_info(cls, fb_user_id):
        try:
            url = 'https://graph.facebook.com/%s?access_token=%s' % (fb_user_id, cls.APP_TOKEN)
            response = rq.get(url, verify=False).json()
            assert response.get('id')
            return response
        except Exception, e:
            logger.error(traceback.format_exc())
            # traceback.print_exc()
            logger.error('Error get , err: %r',  e)
            return None

    @classmethod
    def login_info(cls, token):
        '''
        https://graph.facebook.com/debug_token?access_token=372877603536187|29e68240c95ceddbe0a6798400ce2f0a&
        input_token=EAAFTIVUafTsBAFEDaxP3vODkuCxbdGuxZAhpyDsKYvUUY7jJtIsauhDWyoQm2uIbToY9J07ZCMnrlpZCu0ZBlKWE
        sSHlxp99AmBZCKFE7Juo2Kf4eWdpEyS9gtO30D8Pmq7B22HJfJ8nKJCMRnD3caZCm8NVBIJ3JKjfZBZADar8niZB5JqFrZAcj4U6B
        Dcn8fQfI4XBXCaaZCekhDWhYg7BxdHE1gxyRCfQySJztzc5h71MQbqRRzlsZA9r
        :param token:
        :return:
        '''
        try_times = 3
        for i in range(try_times):
            try:
                user_id = cls._get_user_id(token)
                assert user_id is not None
                return cls._get_info(user_id)
            except Exception, e:
                # Invalid token
                if i < try_times - 1:
                    time.sleep(0.3)
                    continue
                logger.error('log false token:%s, %s', token, e)
                return None
