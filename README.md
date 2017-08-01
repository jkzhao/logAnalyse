# logAnalyse
analyse nginx logs, display data graphically.

# 日志格式
```
log_format ids6 '$http_host $remote_addr [$time_local] $msec "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time $upstream_response_time';
line = 'cas.wisedu.com 172.16.4.91 [26/Jul/2017:10:15:09 +0800] 1501035309.217 "GET /authserver/login?service=http%3A%2F%2Fhrn.wisedu.com%2Fhr HTTP/1.1" 200 6864 "-" "Jakarta Commons-HttpClient/3.1" 0.003 0.003'
```
日志字段说明：
```
$remote_addr, $http_x_forwarded_for 记录客户端IP地址
$remote_user 记录客户端用户名称
$request 记录请求的URL和HTTP协议
$status 记录请求状态
$body_bytes_sent 发送给客户端的字节数，不包括响应头的大小； 该变量与Apache模块mod_log_config里的“%B”参数兼容。
$bytes_sent 发送给客户端的总字节数。
$connection 连接的序列号。
$connection_requests 当前通过一个连接获得的请求数量。
$msec 日志写入时间。单位为秒，精度是毫秒。
$pipe 如果请求是通过HTTP流水线(pipelined)发送，pipe值为“p”，否则为“.”。
$http_referer 记录从哪个页面链接访问过来的
$http_user_agent 记录客户端浏览器相关信息
$request_length 请求的长度（包括请求行，请求头和请求正文）。
$request_time 官网描述：request processing time in seconds with a milliseconds resolution; time elapsed between the first bytes were read from the client and the log write after the last bytes were sent to the client 。
              指的就是从接受用户请求的第一个字节到发送完响应数据的时间，即包括接收请求数据时间、程序响应时间、输出响应数据时间。
$upstream_response_time: 指从Nginx向后端（php-cgi)建立连接开始到接受完数据然后关闭连接为止的时间。
                        从上面的描述可以看出，$request_time肯定比$upstream_response_time值大，特别是使用POST方式传递参数时，因为Nginx会把request body缓存住，接受完毕后才会把数据一起发给后端。
                        所以如果用户网络较差，或者传递数据较大时，$request_time会比$upstream_response_time大很多。
                        所以如果使用nginx的accesslog查看php程序中哪些接口比较慢的话，记得在log_format中加入$upstream_response_time。
$time_iso8601 ISO8601标准格式下的本地时间。
$time_local 通用日志格式下的本地时间。
```

# 批处理 处理日志流程
开始 ——> 读入 ——> 解析 ——> 分析 ——> 展示 ——> 结束

# 分析展示：
1. 流量（字段里有每个页面的长度）       sum                 line chat(线图)
2. TOP 10 URL                    count之后取前10          bar chat(条形图)
3. TOP 10 IP                     count之后取前10          bar chat(条形图)
4. TOP 10 UA                     count之后取前10          bar chat(条形图)
5. 一段时间内状态码的分布               group by            pie chat(饼图，但是不能展示时间，可以选用stack chat，百分比的面积图)
6. UA的分布                           group by            pie chat(饼图，但是不能展示时间，可以选用stack chat，百分比的面积图)
7. http版本的分布（知道了之后可以做对应的一些压缩） group by  pie chat(饼图，但是不能展示时间，可以选用stack chat，百分比的面积图)

# 画图
python画图pygal模块，当然也可以用前端来画
```
pip install pygal
```
