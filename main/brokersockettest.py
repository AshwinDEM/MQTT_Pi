import socket 
import threading

HEADER = 64
PORT_RECEIVE = 5050
PORT_SEND = 5005
SERVER = socket.gethostbyname(socket.gethostname())
ADDR_RECEIVE = (SERVER, PORT_RECEIVE)
ADDR_SEND = (SERVER, PORT_SEND)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

broker_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broker_send.connect(ADDR_SEND)

broker_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broker_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

broker_recv.bind(ADDR_RECEIVE)


# Sending stuff to receivers part
def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	broker_send.send(send_length)
	broker_send.send(message)



# Receiving from servers part

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

			print(f"[{addr}] {msg}")
			send(msg)
			send(DISCONNECT_MESSAGE)

	conn.close()

def start():
	broker_recv.listen()
	print(f"[LISTENING] Broker is listening on {SERVER}")
	while True:
		conn, addr = broker_recv.accept()
		thread = threading.Thread(target = handle_client, args = (conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Main part

def main():
	print("[STARTING] Broker is starting...")
	start()
	send("Hi, Pooja")


if __name__ == "__main__":
	main()