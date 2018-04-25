# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Index, UniqueConstraint, Column, Integer, String
from urllib.parse import quote_plus as urlquote
import re
import os

# 初始化数据库连接
conn_str = 'mysql+pymysql://root:%s@172.16.7.180:3306/mydb' % urlquote('Wisedu@2017')
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
    url = Column(String(500))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(255))
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
    url = Column(String(500))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(255))
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
    url = Column(String(500))
    version = Column(String(10))
    status = Column(String(10))
    length = Column(String(45))
    http_referer = Column(String(1500))
    ua = Column(String(255))
    request_time = Column(String(15))
    upstream_response_time = Column(String(15))

    def __repr__(self): #这个方法其实就是做了：当我在打印某个对象的时候，给我们展示的不会再是对象名称地址的内容了，而是表中那条数据的真实内容>了。当然你也可以只返回self.name
           return "<Desginer_access_log(host='%s', remote_addr='%s', time='%s', method='%s', url='%s', version='%s', " \
                  "status='%s', length='%s', http_referer='%s', ua='%s', request_time='%s', " \
                  "upstream_response_time='%s')>" % ( #但是这只是显示出来，其实还是一个对象
                                self.host, self.remote_addr, self.time, self.method, self.url, self.version, self.status, self.length, self.http_referer, self.ua, self.request_time, self.upstream_response_time)

def init_db():
    '''创建所有表结构'''
    Base.metadata.create_all(engine)
def drop_db():
    '''#删除所有的表，删除的表是当前类对应的表'''
    Base.metadata.drop_all(engine)


def add(line_lst):
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

def main():
    line_lst = []
    for line in read_log(file):
        line_dict = regular_line(line)

        if 'res?' in line_dict['url']: #不同的url分配到三个不同的表中,一个是统计网站的访问，一个是统计移动框架的访问，res?和mf?、Desginer?
            line = Res_access_log(host=line_dict['host'], remote_addr=line_dict['remote_addr'], time=line_dict['time'],
                                  method=line_dict['method'], url=line_dict['url'], version=line_dict['version'],
                                  status=line_dict['status'], length=line_dict['length'],
                                  http_referer=line_dict['http_referer'], ua=line_dict['ua'],
                                  request_time=line_dict['request_time'],
                                  upstream_response_time=line_dict['upstream_response_time']
                                  )
        elif 'mf?' in line_dict['url']:
            line = Mf_access_log(host=line_dict['host'], remote_addr=line_dict['remote_addr'], time=line_dict['time'],
                                  method=line_dict['method'], url=line_dict['url'], version=line_dict['version'],
                                  status=line_dict['status'], length=line_dict['length'],
                                  http_referer=line_dict['http_referer'], ua=line_dict['ua'],
                                  request_time=line_dict['request_time'],
                                  upstream_response_time=line_dict['upstream_response_time']
                                  )
        else:
            line = Desginer_access_log(host=line_dict['host'], remote_addr=line_dict['remote_addr'], time=line_dict['time'],
                                  method=line_dict['method'], url=line_dict['url'], version=line_dict['version'],
                                  status=line_dict['status'], length=line_dict['length'],
                                  http_referer=line_dict['http_referer'], ua=line_dict['ua'],
                                  request_time=line_dict['request_time'],
                                  upstream_response_time=line_dict['upstream_response_time']
                                  )
        line_lst.append(line)

    add(line_lst)

if __name__ == '__main__':
    pattern = '(?P<host>[\w+\.]+\w+) (?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\]'
    pattern += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
    pattern += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'

    path = '/usr/local/nginx/nginx/logs/statistics/'
    filename = 'res.statistics.log-*'
    file_path = os.path.join(path, filename)
    out = os.popen("ls %s | tail -1" % file_path)

    #path = '/usr/local/nginx/nginx/logs/statistics/'
    #filename = 'res.statistics.log-20180323'
    #file_path = os.path.join(path, filename)
    #out = os.popen("/usr/local/openresty/nginx/logs/statistics/res.statistics.log-20180117")
    #out = os.popen("ls %s" % file_path)
    
    file = out.read().replace("\n", "")

    main()

