# -*- coding: utf-8 -*-

import re
import datetime
import threading

def read_log(path):
    '''读日志'''
    with open(path) as f:
        yield from f #打开日志文件，逐行yield出来。yield from f 相当于下面两行代码
        # for line in f:
        #     yield line

def parse(path):
    '''解析日志 use re library to parse logs'''
    pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*.* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"'
    o = re.compile(pattern)
    for line in read_log(path):
        m = o.search(line.rstrip('\n')) #从右边
        if m:
            data = m.groupdict()
            now = datetime.datetime.now()
            data['time'] = now.strptime('%d/%b/%Y:%H:%M:%S %z')
            yield data

def data_source(src, dst, event):
    while not e.is_set(): #不断的产生数据
        with open(dst, 'a') as f:
            for item in parse(src):
                line ='{ip} - - [{time}] "method {url} {version}" {status} {length} "{referer}" "{ua}"\n'.format(**item)
                f.write(line)
                e.wait(0.1) #每隔0.1s产生一条数据

if __name__ == '__main__':
    import sys
    e = threading.Event()  # 流控

    try:
        data_source(sys.argv[1], sys.argv[2], e)
    except KeyboardInterrupt:
        e.set()

