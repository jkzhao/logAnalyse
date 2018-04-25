# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from urllib.parse import quote_plus as urlquote
import yaml

if __name__ == "__main__":
    conn_str = 'mysql+pymysql://root:%s@172.16.7.180:3306/mydb_test' % urlquote('Wisedu@2017')
    engine = sqlalchemy.create_engine(conn_str)
    # 下面这两句话就完成了ORM映射 Base.classes.XXXX即为映射的类
    # Base.metadata.tables['XXX']即为相应的表
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    print(Base.classes.keys())  # 获取所有的对象名
    #print(Base.classes.values())
    # for key in Base.classes.keys():
    #     print(Base.classes.get(key))

    # 获取表对象
    # Res_access_log = Base.classes.res_access_log
    # print(Res_access_log)
    # read yaml file
    with open("log_code.yaml", "r+") as stream:
        try:
            log_code_dict = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for log_code in log_code_dict.keys():
        table_name = log_code_dict.get(log_code)
        if table_name in Base.classes.keys():
            table_class = Base.classes.get(table_name)
            print(table_class)

    # 查询操作
    # session = Session(engine)
    # result = session.query(Res_access_log).all()
    # print(result)
    # for line in result:
    #     print(line.host, line.ua)

    # 插入操作
    # item = Res_access_log(host='172.16.3.78', remote_addr='115.239.212.193', time='23/Mar/2018:04:06:30 +0800',
    #                   method='GET', url='/statistics/res?/&callback=__jp0', version='HTTP/1.1',
    #                   status='200', length='0',
    #                   http_referer='http://res.wisedu.com/', ua='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    #                   request_time='0.000',
    #                   upstream_response_time='')
    # session.add(item)
    # session.commit()

    # session.close()




