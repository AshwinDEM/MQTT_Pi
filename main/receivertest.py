import socket 
import threading

HEADER = 64
PORT = 5005
receiver = socket.gethostbyname(socket.gethostname())
ADDR = (receiver, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver.bind(ADDR)

def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected")
	
	connected = True
	while connected:
		msg_length = conn.recv(HEADER)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False
				break

			print(f"[{addr}] {msg}")

	conn.close()



def start():
	receiver.listen()
	print(f"[LISTENING] receiver is listening on {receiver}")
	while True:
		conn, addr = receiver.accept()
		thread = threading.Thread(target = handle_client, args = (conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] receiver is starting...")
start()

