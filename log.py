# -*- coding: utf-8 -*-

'''
批处理日志
'''

import sys, os
import re
import datetime
import pygal #服务器端渲染，现在一般都是客户端渲染

def read_log(path): # generator
    '''读日志'''
    with open(path) as f:
        yield from f #打开日志文件，逐行yield出来。
        # for line in f:
        #     yield line #你想返回什么就yield什么

def parse(path, pattern): #generator
    '''解析日志 use re library to parse logs'''
    o = re.compile(pattern)
    for line in read_log(path):
        m = o.search(line.rstrip('\n')) #从右边
        if m:
            data = m.groupdict()
            # data['time'] = datetime.datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
            yield data

def count(key, data):
    '''计数函数'''
    # 计数类的都可以这么做，比如ip、UA、状态码等。
    if key not in data:
        data[key] = 0
    data[key] += 1

    return data

def analyse(path, pattern):
    '''分析日志'''
    # ret = {}
    ret = {
        'ip': {},
        'url': {},
        'ua': {},
        'status': {},
        'throughput': 0  # 总流量
    }

    # def init_data():
    #     return {
    #         'ip': {},
    #         'url': {},
    #         'ua': {},
    #         'status': {},
    #         'throughput': 0 #总流量
    #     }

    for item in parse(path, pattern): # 遍历生成器
        # time = item['time'].strftime('%Y%m%d%H%M') #时间窗暂时不用了，精确到分钟，按分钟算总流量
        # if time not in ret.keys():
        #     ret[time] = init_data()
        # data = ret[time]
        for key, value in ret.items():
            if key != 'throughput':
                ret[key] = count(item[key], value)
        ret['throughput'] += int(item['length'])

    return ret

def render_line(name, labels, data):
    line = pygal.Line()
    line.title = name
    line.x_labels = labels
    line.add(name, data)

    return line.render(is_unicode=True)

def render_bar(name, labels, data):
    line_chart = pygal.Bar()
    line_chart.title = 'Top 10 %s' % name
    line_chart.x_labels = labels
    line_chart.add(name, data)

    return line_chart.render(is_unicode=True)

def render_pie(name, data):
    pass

def sort_data(title_name, topN, data):
    ret = []
    for k in sorted(data, key=lambda x: x[1], reverse=True)[:topN]:
        ret.append(k)

    labels = [x[0] for x in ret]
    value = [x[1] for x in ret]
    svg_name = '%s.svg' % title_name
    svg = render_bar(title_name, labels=labels, data=value)
    with open(os.path.join('svgs', svg_name), 'w') as f:  # svg格式的文件是一个图像的文本
        f.write(svg)

def main():
    pattern = '(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\] (?P<msec_time>[\d\.]+)'
    pattern += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
    pattern += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'

    data = analyse(sys.argv[1], pattern)

    data_ip = data['ip']
    data_url = data['url']
    data_ua = data['ua']
    data_status = data['status']
    data_throughput = data['throughput']

    sort_data('IP', 10, list(data_ip.items()))
    sort_data('url', 10, list(data_url.items()))
    sort_data('ua', 10, list(data_ua.items()))
    sort_data('status', 5, list(data_status.items()))


    # # render_line('throughput', data['throughput']) #流量
    # rs = list(data.items()) #字典转换成列表
    # rs.sort(key=lambda x: x[0]) #[('301608100320', {'status':{'404':2},'ip':{...},'throughput': 1553259,..}),()]
    # labels = [x[0] for x in rs]
    # throughput = [x[1]['throughput'] for x in rs]
    # # print(len(throughput))
    #
    # svg = render_line('throughput', labels=labels, data=throughput)
    # with open('throughput.svg', 'w') as f: # svg格式的文件是一个图像的文本
    #     f.write(svg)

if __name__ == '__main__':
    main()

