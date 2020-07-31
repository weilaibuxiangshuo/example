#/failsearch/(\d+)/(\d+)/
#'/index/?ran=0.9795003618146258'
#/login/6/
#HTTPServerRequest(protocol='http', host='127.0.0.1:8099', method='PUT', uri='/whitelist/', version='HTTP/1.1', remote_ip='127.0.0.1')


aa = '/index/?ran=0.9795003618146258'
print(aa.split("?"))
print(eval(repr('^'+aa+'$')))
import re

reg = re.compile(eval(repr(aa)))
print(reg.match('/index/'))