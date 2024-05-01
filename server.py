import socket
import threading
import sys

indirizzo_ip = "127.0.0.1"
porta = 60466
lunghezza_header = 10

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

ctrl_c_thread = threading.Thread(target=controllo_ctrl_c)
ctrl_c_thread.daemon = True
ctrl_c_thread.start()

def gestisci_cliente(client_socket, nome_utente):
    try:
        while True:
            messaggio = client_socket.recv(1024)
            if not messaggio:
                print(f'Connessione chiusa da: {nome_utente}')
                break

            for destinatario_socket in connected_clients.items():
                if destinatario_socket != client_socket:
                    destinatario_socket.send(messaggio)

    except Exception as e:
        print(f'Errore nella gestione del client {nome_utente}: {str(e)}')

    finally:
        client_socket.close()
        del connected_clients[client_socket]


while True:
    client_socket, client_address = socket_del_server.accept()
    nome_utente = client_socket.recv(1024).decode()
    connected_clients[client_socket] = nome_utente
    print(f'Nuovo utente connesso {client_address}, nome: {nome_utente}')
    client_thread = threading.Thread(target=gestisci_cliente, args=(client_socket, nome_utente))
    client_thread.start()