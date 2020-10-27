"""
pass
"""
from socket import socket
from time import sleep

s=socket()
s.bind(('0.0.0.0',8989))
s.listen(5)
conn,addr =s.accept()
data = conn.recv(1024)
print(data.decode())
tem = data.decode().split(' ',2)
print(tem)
version = 'HTTP/1.1 '
response_code = '100 gotit \r\n'
response_head ={'Content-Type':'text/html\r\n'}
response_none='\r\n'
if tem[1] == '/python':
	response_code = '200 OK \r\n'
	file=open('./python.html','rb')
	while True:
		data = file.read(10240)
		if not data:
			sleep(0.1)
			break
		response = version+response_code+str(response_head)+response_none
		conn.send(response.encode()+data)
	file.close()
else:
	response_code = '404 not found \r\n'
	data = 'sorry,there has a trouble '
	response = version + response_code + str(response_head) + response_none + data
	conn.send(response.encode())
conn.close()
s.close()