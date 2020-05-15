# coding=utf-8
import json
import time

from ..const import (
    SYS_FORBID_TIME,
    OSS_AUDIO_URL,
    OSS_PIC_URL,
    FEED_NOT_FOUND_ERROR
)
from ..model import (
    Report,
    Feed,
    TrackSpamRecord,
    UserSetting,
    BlockedDevices,
    UserRecord, Blocked
)
from ..service import (
    UserService,
    GlobalizationService,
    ForbidCheckService,
    SpamWordCheckService
)
from ..util import (
    unix_ts_string
)


class ForbidRecordService(object):
    @classmethod
    def mark_record(cls, user_id, from_ts=None, to_ts=None):
        TrackSpamRecordService.mark_spam_word(user_id, from_ts, to_ts)
        return ReportService.mark_report(user_id, from_ts, to_ts)

    @classmethod
    def record_sensitive_device(cls, user_id):
        user_setting = UserSetting.get_by_user_id(user_id)
        if not BlockedDevices.get_by_device(user_setting.uuid):
            BlockedDevices.add_sensitive_device(user_setting.uuid)

    @classmethod
    def get_device_forbidden_num_by_uid(cls, user_id):
        """根据 user_id，返回该设备上的各用户历史封号次数"""
        uuid = UserSetting.uuid_by_user_id(user_id)
        if not uuid:
            return 0
        uids = UserSetting.get_uids_by_uuid(uuid)

        def add(x, y):
            return x + y

        return reduce(add, map(UserRecord.get_forbidden_num_by_uid, uids))

    @classmethod
    def get_forbid_history_by_uid(cls, user_id):
        # 4个位置影响forbid_score，1.敏感用户 2.举报 3.警告 4.其他用户拉黑
        user_record = UserRecord.objects(user_id=user_id).order_by('-create_time').first()
        forbidden_from = user_record.create_time

        is_sensitive = ForbidCheckService.check_sensitive_user(user_id)

        reports = Report.get_report_by_time_and_uid(user_id, forbidden_from - SYS_FORBID_TIME, forbidden_from,
                                                    True)
        region = reports[0].region
        reports_res = []
        for report in reports:
            reports_res.append(ReportService.get_report_info(report))

        blocker_num = Blocked.get_blocker_num_by_time(user_id, forbidden_from - SYS_FORBID_TIME, forbidden_from)

        spam_records = TrackSpamRecord.get_records_by_uid_and_time(user_id, forbidden_from - SYS_FORBID_TIME,
                                                                   forbidden_from)
        record_res = []
        for record in spam_records:
            record_res.append(TrackSpamRecordService.get_spam_record_info(record))

        return {'sensitive': is_sensitive, 'blocker_num': blocker_num, 'reports': reports_res, 'records': record_res}


class ReportService(object):

    @classmethod
    def save_report(cls, user_id, reason, pics=None, target_user_id=None, related_feed_id=None, match_type=None,
                    chat_record=None, dealed=False):
        """举报内容入库"""
        report = Report()
        report.uid = user_id
        report.reason = reason
        report.pics = pics
        report.chat_record = chat_record
        report.related_feed = related_feed_id
        report.region = GlobalizationService.get_region()
        # if target_user_id.startswith('love'):
        #     target_user_id = UserService.uid_by_huanxin_id(target_user_id)
        if dealed:
            report.dealed = dealed
        report.target_uid = target_user_id
        report.create_ts = int(time.time())
        report.save()
        return report.id

    @classmethod
    def mark_report(cls, user_id, from_time=None, to_time=None):
        """
        将一段时间举报user_id的记录标位‘已处理’，参数时间都是时间戳(int)
        :return: 一个集合，包含举报该user的举报者们
        """
        if from_time and to_time:
            objs = Report.objects(target_uid=user_id, create_ts__gte=from_time, create_ts__lte=to_time, dealed=False)
        else:
            objs = Report.objects(target_uid=user_id, create_ts__lte=int(time.time()), dealed=False)
        report_users = set()
        for obj in objs:
            obj.dealed = True
            report_users.add(obj.uid)
            obj.save()
        return report_users

    @classmethod
    def get_report_info(cls, report):
        tmp = {'report_id': str(report.id),'forbid_weight': 2 if report.reason == 'match' else 4, 'reporter': report.uid, 'pics': [OSS_PIC_URL + pic for pic in report.pics],
               'region': report.region, 'chat_record': None, 'reason': report.reason, 'feed': None,
               'reporter_ban_before': UserRecord.get_forbidden_num_by_uid(report.uid) > 0}

        if report.related_feed:
            feed = Feed.objects(id=report.related_feed).first()
            if not feed:
                tmp['feed'] = FEED_NOT_FOUND_ERROR
            tmp['feed'] = {'content': feed.content, 'pics': [OSS_PIC_URL + pic for pic in feed.pics], 'audios':[OSS_AUDIO_URL + audio for audio in feed.audios]}

        if report.chat_record:
            res_record = []
            chat_records = json.loads(report.chat_record)
            for chat_record in chat_records:
                uid = UserService.uid_by_huanxin_id(chat_record['id'])
                res_record.append("%s: %s" % (UserService.nickname_by_uid(uid), chat_record['content']))
            tmp['chat_record'] = '\n'.join(res_record)
        return tmp

    @classmethod
    def info_by_id(cls, report_id):
        report = Report.get_by_id(report_id)
        if not report:
            return u'worng id', False
        return cls.get_report_info(report), True


class TrackSpamRecordService(object):

    @classmethod
    def save_record(cls, user_id, word=None, pic=None, forbid_weight=0):
        if not word and not pic:
            return False
        # if cls.check_spam_word_in_one_minute(user_id, int(time.time())):
        #     return False
        return TrackSpamRecord.create(user_id, word, pic, forbid_weight=forbid_weight)

    # @classmethod
    # def check_spam_word_in_one_minute(cls, user_id, ts):
    #     """检查两条spam_word之间的间隔是不是在1min之内，是的话不入库"""
    #     if TrackSpamRecord.count_by_time_and_uid(user_id, ts - 60, ts) > 0:
    #         return True
    #     return False

    @classmethod
    def mark_spam_word(cls, user_id, from_time=None, to_time=None):
        """将一段时间user_id的track_spam_record记录标位‘已处理’，参数时间都是时间戳(int)"""
        if from_time and to_time:
            objs = TrackSpamRecord.objects(user_id=user_id, create_time__gte=from_time, create_time__lte=to_time,
                                           dealed=False)
        else:
            objs = TrackSpamRecord.objects(user_id=user_id, create_time__lte=int(time.time()), dealed=False)
        for obj in objs:
            obj.dealed = True
            obj.save()

    @classmethod
    def get_review_pic(cls, num=10000):
        """按时间倒序，返回需要review的spam record, [{'pic':'','record_id':''},{'pic':'','record_id':''}]"""
        records = TrackSpamRecord.get_review_pic(num)
        res = []
        for record in records:
            temp = {'pic': record.pic, 'record_id': str(record.id)}
            res.append(temp)
        return res

    @classmethod
    def get_spam_record_info(cls, record):
        tmp = {'forbid_weight': record.forbid_weight,'record_id':record.id, 'create_time':unix_ts_string(record.create_time)}
        if record.word:
            tmp['word'] = {'word': record.word, 'hit_word': SpamWordCheckService.get_spam_word(record.word, GlobalizationService.get_region_by_user_id(record.user_id))}
        elif record.pic:
            tmp['pic'] = {'pic': record.pic}
        return tmp
