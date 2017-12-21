# -*- coding: utf-8 -*-

import re
import pprint #格式化输出
from influxdb import InfluxDBClient


# 一条日志如下：
# log_format ids6 '$http_host $remote_addr [$time_local] $msec "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time $upstream_response_time';
# line = 'cas.wisedu.com 172.16.4.91 [26/Jul/2017:10:15:09 +0800] "GET /authserver/login?service=http%3A%2F%2Fhrn.wisedu.com%2Fhr HTTP/1.1" 200 6864 "-" "Jakarta Commons-HttpClient/3.1" 0.003 0.003'
# line ='res.wisedu.com 172.16.6.4 [14/Dec/2017:09:20:17 +0800] "GET /statistics/res?/bh_apis/1.0/module-bhMenu.html&callback=__jp0 HTTP/1.1" 200 0 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" 0.000 -'

# pattern4 = r'(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\] (?P<msec_time>[\d\.]+) "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+) "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'
# 一行表达式太长了，python 语法有 \ 续行 符号，但是不适合正则表达式
# pattern4 = '(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\]'
# pattern4 += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
# pattern4 += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'
# o = re.compile(pattern4)
# m = o.search(line)
# print(m.groupdict())
# dict = m.groupdict()
# time = dict['time']
# print(time)
# time = time.split(' ')[0]
# print(time)
# dict['time'] = time
# print(dict)
# pprint.pprint(m.groupdict(), indent=4)
# print(type(m.groupdict()))

# point_dict = {}
# point_dict['measurement'] = 'access_log'
# point_dict['fields'] = dict
# lst = []
# lst.append(point_dict)
# print(lst)


# client = InfluxDBClient(host='116.62.71.126', port=8086, username='root', password='wisedu123', database='mydb')
# client.get_list_database()
# json_body = [
# {
#     "measurement": "interface",
#     "tags": {
#         "path": "addresses123",
#         "element": "linkdin234"
#     },
#     "fields": {
#         "value": 12,
#         "ip": "172.16.4.89"
#     },
#     "time": 1157894123000000456    # "1157894123000000456" #"2009-11-10T23:00:00Z"
# }
# ]
# client.write_points(json_body)
# client.write_points(lst)
# result=client.query('select * from interface;')
# # print(type(result))
# print("Result: {0}".format(result))






def read_log(path): # 生成器generator
    with open(path) as f:
        yield from f #打开日志文件，逐行yield出来。yield from f 相当于下面两行代码
        # for line in f:
        #     yield line #你想返回什么就yield什么

def write_influxDB(lst):
    client.write_points(lst)

def regular_line(line):
    o = re.compile(pattern)
    m = o.search(line)
    field_dict = m.groupdict()

    return field_dict

def main():
    for line in read_log(path):
        field_dict = regular_line(line)
        lst = []
        point_dict = {}
        point_dict['measurement'] = 'res_access_log'
        point_dict['fields'] = field_dict
        lst.append(point_dict)

        write_influxDB(lst)

if __name__ == '__main__':
    pattern = '(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time_local>.*)\]'
    pattern += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
    pattern += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'

    path = "logs/res.statistics.log"
    client = InfluxDBClient(host='116.62.71.126', port=8086, username='root', password='wisedu123', database='mydb')

    main()


'''
# 时间格式转换
#
# UTC时间格式：2014-09-18T10:42:16.126Z
# 普通时间格式：2014-09-18 10:42:16
# >>> import time
# >>> int(time.time()*1000000000)
# 1482389517803608064
import pytz
import datetime
import time
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))

print(utc_to_local('2017-12-15T02:10:19.154429478Z'))
'''

'''
import time

def timestamp_datetime(value):
    #format = '%Y-%m-%d %H:%M:%S'
    format = '%d/%b/%Y:%H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    #time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    time.strptime(dt, '%d/%b/%Y:%H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    #s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    s = time.mktime(time.strptime(dt, '%d/%b/%Y:%H:%M:%S'))
    return int(s)


if __name__ == '__main__':
    #d = datetime_timestamp('2012-03-28 06:53:40')
    d = datetime_timestamp('15/Dec/2017:03:20:17')
    print(d)
    s = timestamp_datetime(1332888820)
    print(s)
'''

