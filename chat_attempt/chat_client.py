import socket

def client_connect(context):
	sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM, socket.IPPROTO_TCP) 
	#первый параметр - семейство протоколов - ipv4
	#второй - тип - потоковый сокет
	#третий - протокол - tcp/udp или 0 - по умолчанию
	
	context.status.set(f"Подключаюсь к {context.ip_string.get()}:{context.port_string.get()}")
	
	address = (context.ip_string.get(), int(context.port_string.get() ) )
	context.address = address
	try:
		sock.connect( address  )
	except socket.error as mes:
		conn = False
		print(mes)
	else:
		conn = True

	if conn:
		context.my_sock = sock
		context.status.set(f"Успешно подключились к {context.ip_string.get()}:{context.port_string.get()}")
		res = True
	else:
		
		context.status.set("Не удалось установить соединение")
		sock.close() #если не получилось, то...
		res = False

	return res

