#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
        # ci serviamo di un dizionario per registrare i client
        indirizzi[client] = client_address
        #diamo inizio all'attività del Thread - uno per ciascun client
        Thread(target=gestice_client, args=(client,)).start()
        

"""La funzione seguente gestisce la connessione di un singolo client."""
def gestice_client(client):  # Prende il socket del client come argomento della funzione.
    nome = client.recv(BUFSIZ).decode("utf8")
    #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
    benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
    
    try:
        client.send(bytes(benvenuto, "utf8"))
        msg = "%s si è unito all chat!" % nome
        #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
        broadcast(bytes(msg, "utf8"))
        #aggiorna il dizionario clients creato all'inizio
        clients[client] = nome
    
        #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
        while True:
            try:
                msg = client.recv(BUFSIZ)
            except (ConnectionAbortedError, ConnectionResetError):
                print("%s:%s si è scollegato prima di entrare nella chat." % indirizzi[client])
                client.close()
                del clients[client]
                break
            
            if msg != bytes("{quit}", "utf8"):
                if msg is not None: #in più
                    broadcast(msg, nome+": ")
            else:
                try:
                    client.send(bytes("{quit}", "utf8"))
                finally:
                    client.close()
                    del clients[client]
                    broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8")) #in più
                    print("%s ha abbandonato la Chat." % nome) #in più
                #except ConnectionResetError:
                    break
    
    except ConnectionResetError:
        print(f'{indirizzi[client]} è uscito dalla chat forzatamente')
    #    broadcast(f"{indirizzi[client]} è uscito dalla chat forzatamente")
        #print("%s si è scollegato forzatamente." % indirizzi[client])
        #clients[client].clear()
        #indirizzi[client].clear()
        

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    if clients: #in più
        for utente in clients:
            utente.send(bytes(prefisso, "utf8")+msg) #era con bytes + msg

        
clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    #SERVER.detach()     #In più