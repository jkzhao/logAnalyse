# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Index, UniqueConstraint, Column, Integer, String
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
Base = declarative_base()  # 生成一个SQLORM基类

#一个类用来生成一张表
class Res_access_log(Base):
    __tablename__ = 'res_access_log' #__tablename__是固定用法，后面的表名自己定义

    #定义表的字段
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    host = Column(String(45))
    remote_addr = Column(String(45))
    time = Column(String(60))
    method = Column(String(45))
    url = Column(String(1300))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(1500))
    request_time = Column(String(15))
    upstream_response_time = Column(String(15))

    def __repr__(self): #这个方法其实就是做了：当我在打印某个对象的时候，给我们展示的不会再是对象名称地址的内容了，而是表中那条数据的真实内容了。当然你也可以只返回self.name
           return "<Res_access_log(host='%s', remote_addr='%s', time='%s', method='%s', url='%s', version='%s', " \
                  "status='%s', length='%s', http_referer='%s', ua='%s', request_time='%s', " \
                  "upstream_response_time='%s')>" % ( #但是这只是显示出来，其实还是一个对象
                                self.host, self.remote_addr, self.time, self.method, self.url, self.version, self.status, self.length, self.http_referer, self.ua, self.request_time, self.upstream_response_time)

class Mf_access_log(Base):
    __tablename__ = 'mf_access_log' #__tablename__是固定用法，后面的表名自己定义

    #定义表的字段
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    host = Column(String(45))
    remote_addr = Column(String(45))
    time = Column(String(60))
    method = Column(String(45))
    url = Column(String(1300))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(1500))
    request_time = Column(String(15))
    upstream_response_time = Column(String(15))

    def __repr__(self): #这个方法其实就是做了：当我在打印某个对象的时候，给我们展示的不会再是对象名称地址的内容了，而是表中那条数据的真实内容了。当然你也可以只返回self.name
           return "<Mf_access_log(host='%s', remote_addr='%s', time='%s', method='%s', url='%s', version='%s', " \
                  "status='%s', length='%s', http_referer='%s', ua='%s', request_time='%s', " \
                  "upstream_response_time='%s')>" % ( #但是这只是显示出来，其实还是一个对象
                                self.host, self.remote_addr, self.time, self.method, self.url, self.version, self.status, self.length, self.http_referer, self.ua, self.request_time, self.upstream_response_time)

class Desginer_access_log(Base):
    __tablename__ = 'desginer_access_log' #__tablename__是固定用法，后面的表名自己定义

    #定义表的字段
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    host = Column(String(45))
    remote_addr = Column(String(45))
    time = Column(String(60))
    method = Column(String(45))
    url = Column(String(1300))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(1500))
    request_time = Column(String(15))
    upstream_response_time = Column(String(15))

    def __repr__(self): #这个方法其实就是做了：当我在打印某个对象的时候，给我们展示的不会再是对象名称地址的内容了，而是表中那条数据的真实内容>了。当然你也可以只返回self.name
           return "<Desginer_access_log(host='%s', remote_addr='%s', time='%s', method='%s', url='%s', version='%s', " \
                  "status='%s', length='%s', http_referer='%s', ua='%s', request_time='%s', " \
                  "upstream_response_time='%s')>" % ( #但是这只是显示出来，其实还是一个对象
                                self.host, self.remote_addr, self.time, self.method, self.url, self.version, self.status, self.length, self.http_referer, self.ua, self.request_time, self.upstream_response_time)

class Weplus_access_log(Base):
    __tablename__ = 'weplus_access_log' #__tablename__是固定用法，后面的表名自己定义

    #定义表的字段
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    host = Column(String(45))
    remote_addr = Column(String(45))
    time = Column(String(60))
    method = Column(String(45))
    url = Column(String(1300))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(1500))
    request_time = Column(String(15))
    upstream_response_time = Column(String(15))

    def __repr__(self): #这个方法其实就是做了：当我在打印某个对象的时候，给我们展示的不会再是对象名称地址的内容了，而是表中那条数据的真实内容>了。当然你也可以只返回self.name
           return "<Weplus_access_log(host='%s', remote_addr='%s', time='%s', method='%s', url='%s', version='%s', " \
                  "status='%s', length='%s', http_referer='%s', ua='%s', request_time='%s', " \
                  "upstream_response_time='%s')>" % ( #但是这只是显示出来，其实还是一个对象
                                self.host, self.remote_addr, self.time, self.method, self.url, self.version, self.status, self.length, self.http_referer, self.ua, self.request_time, self.upstream_response_time)

def init_db():
    '''创建所有表结构'''
    Base.metadata.create_all(engine)
def drop_db():
    '''#删除所有的表，删除的表是当前类对应的表'''
    Base.metadata.drop_all(engine)

#创建一个对象，就相当于在表里面创建一行数据，只是现在还没插入
# line = Res_access_log(host='res.wisedu.com', remote_addr='172.16.40.157', time='15/Dec/2017:09:02:50 +0800',
#                       method='GET', url='/statistics/res?/&callback=__jp0', version='HTTP/1.1', status='304',
#                       length='0', http_referer='http://res.wisedu.com/',
#                       ua='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
#                       request_time='0.000', upstream_response_time='-'
#                       )
# print(line)

#这两行触发sessionmaker类下的__call__方法，return得到 Session实例，赋给变量session，所以session可以调用Session类下的add，add_all等方法

# session.add_all([  #一次生成多个对象
#     Res_access_log(name='alex', fullname='Alex Li', password='456'),
#     Res_access_log(name='alex', fullname='Alex old', password='789'),
#     Res_access_log(name='peiqi', fullname='Peiqi Wu', password='sxsxsx')])
#
# session.commit() #提交，查询不需要commit

def add(line):
    '''批量插入'''
    MySession = sessionmaker(bind=engine)
    session = MySession()
    #session.add_all(line_lst)  # 添加对象进去，也就是往数据库插数据
    session.add(line)
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
    m = __import__('python_mysql', fromlist=True)
    #print(m)
    table_class = getattr(m, table_name)  # 通过反射去模块m中找到代表那张表的类
    logger.debug('对应的类为：%s' % table_class)
    #print(table_class)
    return table_class(host=line_dict['host'], remote_addr=line_dict['remote_addr'], time=line_dict['time'],
                      method=line_dict['method'], url=line_dict['url'], version=line_dict['version'],
                      status=line_dict['status'], length=line_dict['length'],
                      http_referer=line_dict['http_referer'], ua=line_dict['ua'],
                      request_time=line_dict['request_time'],
                      upstream_response_time=line_dict['upstream_response_time']
                     )

def main():
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
                add(line)
    logger.info("日志处理完成。。。")

if __name__ == '__main__':
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

