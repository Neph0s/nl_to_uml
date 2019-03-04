# coding: utf-8
import functools
import logging
import warnings

import bson
from . import error
from flask import (
    current_app,
    g,
    request,
    jsonify,
)

from ..response import guest_forbidden

def _has_user_id():
    if request.user_id is None:
        return None  # 标示session验证时出现了Exception
    else:
        return bson.ObjectId.is_valid(request.user_id)


def session_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if current_app.debug:
            return view(*args, **kwargs)
        has_user_id = _has_user_id()
        if has_user_id:
            if request.is_guest:
                # 游客用户返回460
                return guest_forbidden()
            return view(*args, **kwargs)
        if has_user_id is None:  # 检查时发生了Exception, 报错而不登出.
            return jsonify(error.FailedSession)
    return wrapper


def session_required_with_guest(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if current_app.debug:
            return view(*args, **kwargs)
        has_user_id = _has_user_id()
        if has_user_id:
            return view(*args, **kwargs)
        if has_user_id is None:  # 检查时发生了Exception, 报错而不登出.
            return jsonify(error.FailedSession)
    return wrapper
