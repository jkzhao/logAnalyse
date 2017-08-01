# -*- coding: utf-8 -*-

'''
流式处理日志:
    流处理就是一条条处理，每一条数据之间没关系，流处理天然适合分布式处理，没有共享的数据
'''

import sys
import os
import re
import datetime
import pygal #服务器端渲染，现在一般都是客户端渲染
import threading
import requests


def read_log(path): # 流式读取
    '''读日志'''
    offset = 0
    event = threading.Event
    while not event.is_set():
        with open(path) as f:
            if offset > os.stat(path).st_size: # 文件大小
                offset = 0
            f.seek(offset)
            yield from f
            offset = f.tell()
        event.wait(0.1)

pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*.* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"'
o = re.compile(pattern)
def parse(path):
    '''解析日志 use re library to parse logs'''
    for line in read_log(path):
        m = o.search(line.rstrip('\n'))
        if m:
            data = m.groupdict()
            yield data


def agg(path, interval=10): # 10s聚合一次
    '''聚合日志，流量、count、错误率'''
    count = 0
    traffic = 0
    error = 0
    start = datetime.datetime.now()
    for item in parse(path):
        count += 1
        traffic += int(item['length'])
        if int(item['status'] >= 300):
            error += 1
        current = datetime.datetime.now()
        if (current - start).total_seconds() > interval:
            error_rate = error / count
            # send to influxDB
            send(count, traffic, error_rate)
            start = current
            count = 0
            traffic = 0
            error = 0

def send(count, traffic, error_rate):
    #       key         value                            timestamp不写就是当前时间
    line = 'access_log count={},traffic={},error_rate={}'.format(count, traffic, error_rate)
    # write to influxDB, first create database magedu
    res = requests.post('http://127.0.0.1:8086/write', data=line, params={'db': 'magedu'})
    # create database (或者访问8083端口，也可以访问influxDB)
    # $ influx
    # > CREATE DATABASE magedu
    # > show database
    # > use magedu
    # > show measurements #查看数据

    # 测试
    # if res.status_code >= 300:
    #     print(res.content)

if __name__ == '__main__':
    import sys
    agg(sys.argv[1])

