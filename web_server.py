"""
根据用户的用法封装到类，用户可以直接调用类分享网页
"""
import os
import re
from socket import *
from select import select


class WebModel():
	def __init__(self, addr=('0.0.0.0', 9990), web='./static'):  # 自动执行
		self.addr = addr
		self.web = web
		self.create_socket()
		self.bind()
		self.rlist = []
		self.wlist = []
		self.xlist = []

	def start(self):
		self.rlist.append(self.sock)
		print(self.rlist)
		self.sock.listen(5)
		print("listen to the client")
		while True:
			rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
			for item in rs:
				if item is self.sock:
					conn, client = item.accept()
					print("connect from:", client)
					conn.setblocking(False)
					# self.wlist.append(conn)
					self.rlist.append(conn)
				else:
					try:
						self.handle(conn)
					except:
						pass
					self.rlist.remove(item)
					item.close()
			for item in ws:
				pass

	def create_socket(self):
		self.sock = socket()
		self.sock.setblocking(False)

	def bind(self):
		self.sock.bind(self.addr)

	def handle(self, conn):
		request = conn.recv(1024*10).decode()
		print(request)
		if request:
			pattern = r'\w+\s(?P<info>/\S*)'
			result = re.match(pattern, request)
			info = result.group('info')
			print("请求内容：", info)
			self.send_web(conn, info)
		else:
			return

	def send_web(self, conn, info):
		if info == "/":
			filename = "/index.html"
		# fr=open(self.web+'/index.html','rb')
		else:  # info in os.listdir(self.web)
			filename = info
		try:
			fr = open(self.web + filename, 'rb')
		except:
			response = "HTTP/1.1 404 NOT FOUND\r\n"
			response += "Content-Type:text/html\r\n"
			response += "\r\n"
			response =response.encode()+b"sorry,there has none what you found"
		else:
			content = fr.read()
			response = "HTTP/1.1 200 OK\r\n"
			response += "Content-Type:text/html\r\n"
			response += "\r\n"
			response =response.encode()+ content
		finally:
			conn.send(response)
			fr.close()


if __name__ == '__main__':
	web_share = WebModel()  # 可以传参绑定分享的服务器和网页
	web_share.start()
