# -*- coding: utf-8 -*-

'''
批处理日志
'''

import sys
import re
import datetime
import pygal #服务器端渲染，现在一般都是客户端渲染

def read_log(path): # 生成器generator
    '''读日志'''
    with open(path) as f:
        yield from f #打开日志文件，逐行yield出来。yield from f 相当于下面两行代码
        # for line in f:
        #     yield line #你想返回什么就yield什么

def parse(path): #generator
    '''解析日志 use re library to parse logs'''
    pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*.* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"'
    o = re.compile(pattern)
    for line in read_log(path):
        m = o.search(line.rstrip('\n')) #从右边
        if m:
            data = m.groupdict()
            data['time'] = datetime.datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
            yield data

# def window(time): # 日志里面有时间字段，10/Aug/2016:03:20:09 +0800
#     '''时间窗函数，为了统计流量的数据'''
#     fmt = '%d/%b/%Y:%H:%M:%S %z'
#     dt = datetime.datetime.strptime(time, fmt)
#     dt.strptime('%Y%m%d%H%M')

def count(key, data):
    '''计数函数'''
    # 计数类的都可以这么做，比如ip、UA、状态码等。
    if key not in data:
        data[key] = 0
    data[key] += 1

    return data

def analyse(path):
    '''分析日志'''
    ret = {}

    def init_data():
        return {
            'ip': {},
            'url': {},
            'ua': {},
            'status': {},
            'throughput': 0 #总流量
        }

    for item in parse(path): # 遍历生成器
        time = item['time'].strftime('%Y%m%d%H%M') #时间窗暂时不用了，精确到分钟，按分钟算总流量
        if time not in ret.keys():
            ret[time] = init_data()
        data = ret[time]
        for key, value in data.items():
            if key != 'throughput':
                data[key] = count(item[key], value)
        data['throughput'] += int(item['length'])

    return ret

def render_line(name, labels, data):
    line = pygal.Line()
    line.title = name
    line.x_labels = labels
    line.add(name, data)

    return line.render(is_unicode=True)

def render_bar(name, data):
    pass

def render_pie(name, data):
    pass

def main():
    data = analyse(sys.argv[1])

    # render_line('throughput', data['throughput']) #流量
    rs = list(data.items()) #字典转换成列表
    rs.sort(key=lambda x: x[0]) #[('301608100320', {'status':{'404':2},'ip':{...},'throughput': 1553259,..}),()]
    labels = [x[0] for x in rs]
    throughput = [x[1]['throughput'] for x in rs]
    # print(len(throughput))

    svg = render_line('throughput', labels=labels, data=throughput)
    with open('throughput.svgs', 'w') as f: # svg格式的文件是一个图像的文本
        f.write(svg)

if __name__ == '__main__':
    main()

