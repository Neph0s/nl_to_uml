import os
import sys
import fcntl
import datetime
from hendrix.conf import setting
from litatom.service import AlertService, RetainAnaService
import time
from litatom.util import (
    write_data_to_xls,
    ensure_path,
    now_date_key
)

def run():
    dst_addr = '/data/retain_ana/%s.xlsx' % (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    # dst_addr = '/data/statres/2019-11-15.xlsx'
    ensure_path(dst_addr)
    RetainAnaService.get_res(dst_addr)
    AlertService.send_file(["litatomwang@gmail.com", "w326571@126.com", '382365209@qq.com'], dst_addr)


if __name__ == "__main__":
    run()
