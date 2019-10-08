# coding: utf-8
"""
图片上传下载
"""
import logging

from flask import (
    jsonify,
    request,
    #send_file,
    Response
)

from ...decorator import (
    session_required
)

from ...error import (
    Success,
    Failed,
    FailedLackOfField
)
from ....response import (
    failure,
    fail
)
from ....service import (
    AliOssService,
    QiniuService
)

logger = logging.getLogger(__name__)

@session_required
def upload_image_from_file():
    """
    直接上传图片到云盘
    目前只用来传实名认证图片
    """
    image = request.files.get('image')
    if not image:
        return jsonify(Failed)

    fileid = AliOssService.upload_from_binary(image)
    if not fileid:
        return jsonify(Failed)
    url = 'http://www.litatom.com/api/sns/v1/lit/image/' + fileid
    reason = QiniuService.should_pic_block_from_url(url)
    if reason:
        return fail('the pic have vialate rule of:%s please check' % reason)
    return jsonify({
        'success': True,
        'data': {
            'fileid': fileid
        }
    })

def get_image(fileid):
    if fileid == 'null':
        return jsonify(Failed)
    content = AliOssService.get_binary_from_bucket(fileid)
    if not content:
        return Response('', mimetype='image/jpeg')   # 返回空图片流, 兼容错误
        #return jsonify(Failed)
    return Response(content, mimetype='image/jpeg')

@session_required
def upload_audio_from_file():
    """
    直接上传图片到云盘
    目前只用来传实名认证图片
    """
    audio = request.files.get('audio')
    if not audio:
        return jsonify(Failed)

    fileid = AliOssService.upload_from_binary(audio)
    if not fileid:
        return jsonify(Failed)
    return jsonify({
        'success': True,
        'data': {
            'fileid': fileid
        }
    })

def get_audio(fileid):
    if fileid == 'null':
        return jsonify(Failed)
    content = AliOssService.get_binary_from_bucket(fileid)
    if not content:
        return Response('', mimetype='audio/AMR')   # 返回空流, 兼容错误
    return Response(content, mimetype='audio/AMR')