# -*- coding: utf-8 -*-
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote
import re
import os
import yaml
import logging, logging.config

with open('conf/logging.yml', 'r') as f_conf:
    dict_conf = yaml.load(f_conf)
logging.config.dictConfig(dict_conf)
logger = logging.getLogger('simpleExample')

# 初始化数据库连接
conn_str = 'mysql+pymysql://root:%s@172.16.7.180:3306/mydb_test' % urlquote('Wisedu@2017')
engine = create_engine(conn_str)

def add(line):
    '''单条记录插入'''
    MySession = sessionmaker(bind=engine)
    session = MySession()
    session.add(line)
    session.commit()

def add_bath(line_lst):
    '''批量插入'''
    MySession = sessionmaker(bind=engine)
    session = MySession()
    session.add_all(line_lst)  # 添加对象进去，也就是往数据库插数据
    session.commit()

def read_log(file): # 生成器generator
    with open(file) as f:
        yield from f #打开日志文件，逐行yield出来。yield from f 相当于下面两行代码

def regular_line(line):
    '''分析、提取一行日志'''
    o = re.compile(pattern)
    m = o.search(line)
    line_dict = m.groupdict()

    return line_dict

def generate_line_data(table_name, line_dict):
    '''生成一条数据'''
    if table_name in Base.classes.keys():
        table_class = Base.classes.get(table_name)
        # print(table_class)

    return table_class(host=line_dict['host'], remote_addr=line_dict['remote_addr'], time=line_dict['time'],
                      method=line_dict['method'], url=line_dict['url'], version=line_dict['version'],
                      status=line_dict['status'], length=line_dict['length'],
                      http_referer=line_dict['http_referer'], ua=line_dict['ua'],
                      request_time=line_dict['request_time'],
                      upstream_response_time=line_dict['upstream_response_time']
                     )

def main():
    line_list = []
    #读取配置文件中日志标识及其对应的表名
    # read yaml file
    with open("conf/log_code.yaml", "r+") as stream:
        try:
            log_code_dict = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    logger.info("开始一行一行处理日志。。。")
    for line in read_log(file):
        line_dict = regular_line(line)
        for log_code in log_code_dict.keys():
            if log_code in line_dict['url']: # 根据不同的url标识将记录分配到多个个不同的表中,比如统计网站的访问，统计移动框架的访问，res?和mf?、Desginer?
                line = generate_line_data(log_code_dict.get(log_code), line_dict)
                line_list.append(line)

    try:
        add_bath(line_list)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise
    logger.info("日志处理完成。。。")

if __name__ == '__main__':
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # print(Base.classes.keys())  # 获取所有的对象名

    pattern = '(?P<host>[\w+\.]+\w+) (?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\]'
    pattern += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
    pattern += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'

    path = "conf/"
    filename = 'res.statistics.log'
    #path = '/usr/local/openresty/nginx/logs/statistics/'
    #filename = 'res.statistics.log-*'
    file_path = os.path.join(path, filename)
    #out = os.popen("ls %s | tail -1" % file_path)
    out = os.popen("ls %s" % file_path)
    file = out.read().replace("\n", "")

    main()

