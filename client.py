import socket
import threading
import json

indirizzo_ip = "127.0.0.1"
porta = 60466
lunghezza_header = 10

def ricevi_messaggi(socket_del_client):
    try:
        while 1:
            messaggio = socket_del_client.recv(1024)
            if not messaggio:
                print('Connessione chiusa dal server')
                break
            
            messaggio_decodificato = json.loads(messaggio.decode())
            print(f'{messaggio_decodificato["mittente"]} > {messaggio_decodificato["contenuto"]}')

    except Exception as e:
        print('Errore nella ricezione dei messaggi:', str(e))

    finally:
        socket_del_client.close()

def invia_messaggio(socket_del_client):
    try:
        while 1:
            messaggio = input("> ")
            if messaggio:
                messaggio_da_inviare = json.dumps({"mittente": mio_nome, "contenuto": messaggio})
                socket_del_client.send(messaggio_da_inviare.encode())

    except Exception as e:
        print('Errore nell\'invio dei messaggi:', str(e))

    finally:
        socket_del_client.close()

mio_nome = input("Nome: ")

socket_del_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_del_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_del_client.connect((indirizzo_ip, porta))

# Invio del nome utente al server
socket_del_client.send(mio_nome.encode())

# Avvio dei thread per la ricezione e l'invio dei messaggi
thread_ricevi_messaggi = threading.Thread(target=ricevi_messaggi, args=(socket_del_client,))
thread_invia_messaggi = threading.Thread(target=invia_messaggio, args=(socket_del_client,))
thread_ricevi_messaggi.start()
thread_invia_messaggi.start()