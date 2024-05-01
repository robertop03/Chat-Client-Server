import socket
import threading
import sys

indirizzo_ip = '127.0.0.1'
porta = 60467

socket_del_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_del_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_del_server.bind((indirizzo_ip, porta))
socket_del_server.listen()

connected_clients = {}

print(f'Server in ascolto sul socket {indirizzo_ip}:{porta}')

def controllo_ctrl_c():
    while 1:
        try:
            input()
        except EOFError:
            print("Chiusura del server.")
            for client_socket in connected_clients.keys():
                client_socket.close()
            socket_del_server.close()
            sys.exit(0)

def gestisci_client(client_socket, nome_utente):
    try:
        while 1:
            messaggio = client_socket.recv(1024)

            for destinatario_socket, _ in connected_clients.items():
                if destinatario_socket != client_socket:
                    destinatario_socket.send(messaggio)

    except Exception as _:
        print(f'Il client {nome_utente} si è disconnesso')

    finally:
        client_socket.close()
        del connected_clients[client_socket]


ctrl_c_thread = threading.Thread(target=controllo_ctrl_c)
ctrl_c_thread.daemon = 1
ctrl_c_thread.start()

while 1:
    client_socket, client_address = socket_del_server.accept()
    nome_utente = client_socket.recv(1024).decode()
    connected_clients[client_socket] = nome_utente
    print(f'Nuovo utente connesso {client_address}, nome: {nome_utente}')
    client_thread = threading.Thread(target=gestisci_client, args=(client_socket, nome_utente))
    client_thread.start()