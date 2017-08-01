# -*- coding: utf-8 -*-
import re

# 可以看官方文档查看re库的用法，https://docs.python.org/3.5/library/index.html
o = re.compile(r'^a') #r''代表自然字符串，里面的数据不会被转义，compile可做可不做，做了可以提高速度
print(o) #这个o就是已经编译好了的正则表达式
print(help(o.match)) #match从第一个字符处匹配，不匹配就返回None
print(help(o.search)) #search是全文搜索的，但是search有个参数pos，从pos开始。
print(help(o.groups)) #分组
print(help(o.findall))
# match和search的区别
o = re.compile(r'a')
print(o.match('aaa')) #<_sre.SRE_Match object; span=(0, 1), match='a'>
print(o.match('bbb')) #返回None
print(o.match('baba')) #返回None
print(o.search('aaa')) #<_sre.SRE_Match object; span=(0, 1), match='a'>
print(o.search('bbb')) #返回None
print(o.search('baba')) #<_sre.SRE_Match object; span=(1, 2), match='a'>
# 所以match用的少，search用的多。而且正则里面本来^就代表以什么开头

# 正则表达式里有个概念叫"捕获"，就是加()
o = re.compile('(test)')
m = o.search('this is test string, test test test')
print(help(m.group))
print(m.group()) #test
print(m.groups()) #('test',)  返回一个元组
# 这个捕获很类似shell中sed，比如 echo 'this is test' | sed 's/\(test\)/\1xxx/g'  \1就是捕获到的test
# 还有个叫 "命名捕获"  (?P<name>...)
o = re.compile(r'(?P<name>\d+)')
m = o.search('127.0.0.1')
print(m.group()) #127
print(m.groups()) #('127',)
print(m.groupdict()) #{'name': '127'}

# 一条日志如下：
# 66.249.69.131 - - [10/Aug/2016:03:20 +0800] "GET /robots.txt HTTP/1.1" 404 162 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
line = '66.249.69.131 - - [10/Aug/2016:03:20 +0800] "GET /robots.txt HTTP/1.1" 404 162 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
pattern1 = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
# o = re.compile(pattern1)
# m = o.search(line)
# print(m.groupdict()) #{'ip': '66.249.69.131'}


pattern2 = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*.*\[(?P<time>.*)\]'
# o = re.compile(pattern2)
# m = o.search(line)
# print(m.groupdict()) #{'ip': '66.249.69.131', 'time': '10/Aug/2016:03:20 +0800'}

# \w+ 代表字符, \S 代表非空白字符, \s匹配任何空白字符，包括空格、制表符、换页符等等。^ 匹配输入字符串的开始位置，除非在方括号表达式中使用，此时它表示不接受该字符集合。
# []是定义匹配的字符范围。比如 [a-zA-Z0-9] 表示相应位置的字符要匹配英文字符和数字。[\s*]表示空格或者*号。
# [\w|/\.\d]*   [\w\/\.\d]*
# 开头的 r 表示不转义 \
pattern3 = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*.* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"'
o = re.compile(pattern3)
m = o.search(line)
print(m.groupdict())

import pprint #格式化输出
pprint.pprint(m.groupdict(), indent=4)

# 测试文件，把不匹配的行打印出来
# with open('logs/access.log-20160811') as f:
#     total = 0
#     match = 0
#     for line in f:
#         total = total + 1
#         if o.search(line):
#             match = match + 1
#         else:
#             print(line)
# print(total)
# print(match)
print('==============================================\n')



'''
ids.access.log
'''
# () 是为了提取匹配的字符串。表达式中有几个()就有几个相应的匹配字符串。
# (\s*)表示连续空格的字符串。
# []是定义匹配的字符范围。比如 [a-zA-Z0-9] 表示相应位置的字符要匹配英文字符和数字。[\s*]表示空格或者*号。
# {}一般用来表示匹配的长度，比如 \s{3} 表示匹配三个空格，\s[1,3]表示匹配一到三个空格。
# (0-9) 匹配 '0-9′ 本身。 [0-9]* 匹配数字（注意后面有 *，可以为空）[0-9]+ 匹配数字（注意后面有 +，不可以为空）{1-9} 写法错误。
# [0-9]{0,9} 表示长度为 0 到 9 的数字字符串
# *重复零次或更多次
# +重复一次或更多次
# ?重复零次或一次
# {n}重复n次
# {n,}重复n次或更多次
# {n,m}重复n到m次

# 一条日志如下：
# log_format ids6 '$http_host $remote_addr [$time_local] $msec "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time $upstream_response_time';
line = 'cas.wisedu.com 172.16.4.91 [26/Jul/2017:10:15:09 +0800] 1501035309.217 "GET /authserver/login?service=http%3A%2F%2Fhrn.wisedu.com%2Fhr HTTP/1.1" 200 6864 "-" "Jakarta Commons-HttpClient/3.1" 0.003 0.003'
# pattern4 = r'(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\] (?P<msec_time>[\d\.]+) "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+) "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'
# 一行表达式太长了，python 语法有 \ 续行 符号，但是不适合正则表达式
pattern4 = '(?P<host>[\w+\.]+\w+) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(?P<time>.*)\] (?P<msec_time>[\d\.]+)'
pattern4 += ' "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w\/\d\.]*)" (?P<status>\d+) (?P<length>\d+)'
pattern4 += ' "(?P<http_referer>[^\s]*)" "(?P<ua>.*)" (?P<request_time>[\d\.]*) (?P<upstream_response_time>[\d\.]*)'
o = re.compile(pattern4)
m = o.search(line)
# print(m.groupdict())
pprint.pprint(m.groupdict(), indent=4)


