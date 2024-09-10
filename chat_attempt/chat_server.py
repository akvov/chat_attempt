import socket

def local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def server_listen_for_connect(context):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try: 
		sock.bind( (context.ip_string.get(), int(context.port_string.get() )  ) )
	except socket.WinError as mes: #выводим в случае ошибки
		print(mes)
	except socket.error as mes:
		print(mes)


	context.status.set(f"{local_ip()}:{context.port_string.get()} слушает " )
	
	try:
		sock.listen(10) #параметр - размер очереди/число непринятых соединений
	except socket.error as mes:
		print(mes)

	conn, address = sock.accept()
	context.my_sock = conn #запоминаем сокет

	if conn:
		context.status.set(f"Подключился {address}")
		res = True
	else:
		res = False
		context.status.set("Не удалось установить соединение")
		sock.close() #если не получилось, то...

	return res
